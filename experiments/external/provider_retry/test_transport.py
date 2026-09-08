from pathlib import Path
from types import SimpleNamespace
import json
import sys

import pytest

from experiments.external.provider_retry import transport as t


class ServerError(Exception):
    code = 504


@pytest.fixture
def recorder(tmp_path):
    return t.Recorder(tmp_path, {'version':'test','request_timeout_s':600,
                      'cooldown_base_s':300,'cooldown_max_s':1800})


SPEC = SimpleNamespace(provider='google',model='test-model')
USER = 'RECEIVER — call `compute` on the RIGHT type\nsecret prompt body'


def events(recorder):
    return [json.loads(line) for p in recorder.root.glob('events-*.jsonl')
            for line in p.read_text().splitlines()]


def test_failed_request_persists_cooldown_and_skips_without_call(recorder):
    calls=[]
    def fail(*args):
        calls.append(args)
        raise ServerError('secret response')
    with pytest.raises(ServerError):
        recorder.invoke(fail,SPEC,'secret system',USER)
    restarted=t.Recorder(recorder.root,recorder.policy)
    with pytest.raises(t.ProviderCooldown,match='no request sent'):
        restarted.invoke(fail,SPEC,'secret system',USER)
    assert len(calls)==1
    assert events(recorder)[-1]['event']=='cooldown_deferred'
    logged=''.join(p.read_text() for p in recorder.root.glob('events-*.jsonl'))
    assert 'secret' not in logged


def test_success_after_cooldown_resets_streak_and_preserves_inputs(recorder):
    key=t.sha([SPEC.provider,SPEC.model,'system',USER])
    t.atomic(recorder.root/'requests'/f'{key}.json',{'consecutive_transient':4,'retry_after':0})
    calls=[]
    def success(*args):
        calls.append(args)
        return 'unchanged generated code'
    assert recorder.invoke(success,SPEC,'system',USER)=='unchanged generated code'
    assert calls==[(SPEC,'system',USER)]
    state=json.loads((recorder.root/'requests'/f'{key}.json').read_text())
    assert state['consecutive_transient']==0
    assert state['retry_after']==0


def test_different_prompts_do_not_share_cooldown(recorder):
    def fail(*args):raise ServerError()
    with pytest.raises(ServerError):recorder.invoke(fail,SPEC,'s',USER)
    assert recorder.invoke(lambda *args:'ok',SPEC,'changed',USER)=='ok'


def test_same_request_lock_prevents_duplicate(recorder):
    def outer(*args):
        with pytest.raises(t.ProviderCooldown,match='already active'):
            recorder.invoke(lambda *args:pytest.fail('duplicate'),*args)
        return 'ok'
    assert recorder.invoke(outer,SPEC,'s',USER)=='ok'


def test_sdk_attempt_measured_and_headers_not_logged(recorder):
    req=SimpleNamespace(data={'contents':'private'},timeout=600,
                        headers={'X-Server-Timeout':'600','Authorization':'secret-key'})
    observed=[]
    def send(client,request,stream=False):
        observed.append((client,request,stream))
        raise ServerError('private server payload')
    def invoke(*args):return t.sdk_wrapper(send)('client',req)
    with pytest.raises(ServerError):recorder.invoke(invoke,SPEC,'s',USER)
    sdk=[e for e in events(recorder) if e['event'].startswith('sdk_')]
    assert [e['event'] for e in sdk]==['sdk_attempt_start','sdk_attempt_error']
    assert sdk[1]['http_status']==504
    assert sdk[1]['actual_timeout_s']==600
    assert observed==[('client',req,False)]
    assert 'private' not in json.dumps(sdk) and 'secret-key' not in json.dumps(sdk)


def test_delay_is_bounded(recorder):
    for n in [1,2,3,4,20,1000]:
        assert min(300*2**min(n-1,16),1800)<=t.delay(n,recorder.policy)<=1800


def test_non_google_untouched(recorder):
    assert recorder.invoke(lambda *args:'ok',SimpleNamespace(provider='other'),'s','u')=='ok'
    assert events(recorder)==[]


def test_install_does_not_enroll_generated_scripts(tmp_path,monkeypatch):
    p=tmp_path/'policy.json';p.write_text(json.dumps({'enabled':True}))
    monkeypatch.setattr(sys,'argv',['api_test.py'])
    assert t.install(p) is False


def test_install_uses_actual_sdk_without_network(tmp_path,monkeypatch):
    import aideal.llm as llm
    from google.genai import _api_client
    p=tmp_path/'policy.json';config=tmp_path/'config.yaml'
    policy={'enabled':True,'version':'transport-v2','config':str(config),'output':str(tmp_path/'logs'),
            'request_timeout_s':600,'sdk_attempts':1,'cooldown_base_s':300,'cooldown_max_s':1800,
            'sdk_versions':{n:t.importlib.metadata.version(n) for n in ['google-genai','langchain-google-genai']}}
    p.write_text(json.dumps(policy))
    monkeypatch.setattr(sys,'argv',['-m','--config',str(config),'comprehension','--resume','--max-fix-rounds','0'])
    monkeypatch.setattr(llm,'invoke_text',lambda *args:'returned code')
    monkeypatch.setattr(llm,'_transport_retry_installed',False,raising=False)
    monkeypatch.setattr(_api_client.BaseApiClient,'_request_once',_api_client.BaseApiClient._request_once)
    monkeypatch.setenv('AIDEAL_GOOGLE_REQUEST_TIMEOUT_S','300')
    monkeypatch.setenv('AIDEAL_GOOGLE_MAX_RETRIES','2')
    assert t.install(p)
    assert llm.invoke_text(SPEC,'s',USER)=='returned code'
    assert t.os.environ['AIDEAL_GOOGLE_REQUEST_TIMEOUT_S']=='600'
    assert t.os.environ['AIDEAL_GOOGLE_MAX_RETRIES']=='1'
    assert any(json.loads(l)['event']=='worker_enrolled' for f in (tmp_path/'logs').glob('*.jsonl') for l in f.read_text().splitlines())


def test_real_sdk_sends_one_600_second_attempt_with_mock_transport(recorder,monkeypatch):
    import httpx
    from google import genai
    from google.genai import _api_client, types, errors
    requests=[]
    def server(request):
        requests.append(request)
        return httpx.Response(504,json={'error':{'code':504,'message':'test deadline','status':'DEADLINE_EXCEEDED'}})
    client=genai.Client(api_key='offline-test-placeholder')
    client._api_client._httpx_client.close()
    client._api_client._httpx_client=httpx.Client(transport=httpx.MockTransport(server))
    monkeypatch.setattr(_api_client.BaseApiClient,'_request_once',sdk_wrapper_for_test := t.sdk_wrapper(_api_client.BaseApiClient._request_once))
    def invoke(*args):
        return client.models.generate_content(model='gemini-3.1-pro-preview',contents='test',
             config=types.GenerateContentConfig(http_options=types.HttpOptions(timeout=600000,
                                        retry_options=types.HttpRetryOptions(attempts=1))))
    try:
        with pytest.raises(errors.ServerError):recorder.invoke(invoke,SPEC,'s',USER)
        assert len(requests)==1
        assert requests[0].headers['X-Server-Timeout']=='600'
        assert requests[0].extensions['timeout']['read']==600
        assert sum(e['event']=='sdk_attempt_start' for e in events(recorder))==1
    finally:
        client.close()
