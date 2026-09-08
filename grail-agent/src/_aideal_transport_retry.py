"""Opt-in transport wrapper for naturally restarted baseline workers.

No prompt text, credentials, URL queries or request headers are logged.
This adapter has its own policy/code hashes; it is NOT part of the historical
native fingerprint. Reports must retain that transport-treatment distinction.
"""
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
import fcntl
import hashlib
import importlib.metadata
import json
import os
import random
import re
import sys
import time
import uuid

CONTEXT = ContextVar('aideal_transport_request', default=None)


class ProviderCooldown(RuntimeError):
    """Resumable provider outcome; no request was sent and no fix round used."""


def sha(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def atomic(path, value):
    tmp = path.with_name(path.name + f'.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def delay(failures, policy):
    base = min(policy['cooldown_max_s'], policy['cooldown_base_s'] * 2 ** min(failures-1, 16))
    return min(policy['cooldown_max_s'], base + random.uniform(0, base * .1))


class Recorder:
    def __init__(self, root, policy):
        self.root, self.policy = Path(root), policy
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / 'requests').mkdir(exist_ok=True)
        self.metadata = {'transport_version': policy['version'], 'policy_sha256': sha(policy),
                         'adapter_sha256': sha(Path(__file__).read_bytes()), 'pid': os.getpid()}

    def event(self, kind, **fields):
        record = dict(self.metadata, event=kind, epoch=time.time(), **fields)
        # Per-process journal plus flock also protects threads and PID reuse.
        with (self.root / f'events-{os.getpid()}.jsonl').open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.write(json.dumps(record, sort_keys=True) + '\n')
            stream.flush()

    def invoke(self, original, spec, system, user):
        if spec.provider.lower() != 'google':
            return original(spec, system, user)
        key = sha([spec.provider, spec.model, system, user])
        match = re.search(r'RECEIVER\s+—\s+call `([^`]+)`', user)
        api = match[1] if match else None
        context = {'invocation_id': uuid.uuid4().hex, 'request_key': key, 'api': api,
                   'model': f'{spec.provider}:{spec.model}',
                   'prompt_chars': len(system)+len(user), 'prompt_sha256': sha([system, user]),
                   'request_timeout_s': self.policy['request_timeout_s'], 'sdk_attempts': 1,
                   'outer_deadline_s': self.policy['request_timeout_s'] + 30}
        state_path = self.root / 'requests' / f'{key}.json'
        with state_path.with_suffix('.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                self.event('admission_deferred', **context, reason='identical request already active')
                raise ProviderCooldown('Identical request already active; no request sent')
            state = json.loads(state_path.read_text()) if state_path.exists() else {}
            if state.get('retry_after', 0) > time.time():
                self.event('cooldown_deferred', **context, retry_after=state['retry_after'],
                           previous_code=state.get('last_code'))
                raise ProviderCooldown(f"Previous provider {state.get('last_code')}; retry after epoch "
                                       f"{state['retry_after']:.3f}; no request sent")
            started = time.monotonic()
            self.event('invocation_start', **context, previous_end_epoch=state.get('ended_at'))
            token = CONTEXT.set((self, context))
            try:
                response = original(spec, system, user)
            except BaseException as exc:
                code = getattr(exc, 'code', None)
                code = code if isinstance(code, int) else None
                transient = code in (408,429,500,502,503,504) or isinstance(exc, TimeoutError)
                failures = state.get('consecutive_transient', 0) + 1 if transient else 0
                ended = time.time()
                state.update(consecutive_transient=failures, last_code=code,
                             ended_at=ended, retry_after=ended+delay(failures,self.policy) if transient else 0)
                atomic(state_path, state)
                self.event('invocation_error', **context, error_type=type(exc).__name__, http_status=code,
                           wall_s=time.monotonic()-started, retry_after=state['retry_after'])
                raise
            else:
                ended = time.time()
                atomic(state_path, {'consecutive_transient':0,'retry_after':0,'ended_at':ended})
                self.event('invocation_success', **context, wall_s=time.monotonic()-started,
                           response_sha256=sha(response.encode()))
                return response
            finally:
                CONTEXT.reset(token)


def sdk_wrapper(original):
    """Observe each actual synchronous SDK attempt, not only LangChain invoke."""
    @wraps(original)
    def wrapped(client, request, stream=False):
        active = CONTEXT.get()
        if active is None:
            return original(client, request, stream)
        recorder, context = active
        attempt = dict(context, sdk_attempt_id=uuid.uuid4().hex,
                       payload_sha256=sha(request.data), actual_timeout_s=request.timeout,
                       server_timeout_s=request.headers.get('X-Server-Timeout'))
        recorder.event('sdk_attempt_start', **attempt)
        started = time.monotonic()
        try:
            result = original(client, request, stream)
        except BaseException as exc:
            code = getattr(exc, 'code', None)
            recorder.event('sdk_attempt_error', **attempt, error_type=type(exc).__name__,
                           http_status=code if isinstance(code,int) else None,
                           wall_s=time.monotonic()-started)
            raise
        recorder.event('sdk_attempt_success', **attempt, wall_s=time.monotonic()-started)
        return result
    return wrapped


def install(policy_path):
    policy_path = Path(policy_path)
    policy = json.loads(policy_path.read_text())
    # Only explicitly enrolled baseline CLI invocations; never generated test scripts.
    args = sys.argv
    if not policy.get('enabled') or 'comprehension' not in args or '--resume' not in args:
        return False
    if '--config' not in args or '--max-fix-rounds' not in args:
        return False
    if args[args.index('--max-fix-rounds')+1] != '0':
        return False
    if str(Path(args[args.index('--config')+1]).resolve()) != policy['config']:
        return False
    if policy['request_timeout_s'] != 600 or policy['sdk_attempts'] != 1:
        raise ValueError('Unregistered transport timing policy')
    if policy['cooldown_base_s'] <= 0 or policy['cooldown_max_s'] < policy['cooldown_base_s']:
        raise ValueError('Invalid cooldown range')
    versions = {name:importlib.metadata.version(name) for name in policy['sdk_versions']}
    if versions != policy['sdk_versions']:
        raise ValueError('SDK version changed; adapter review required')
    import aideal.llm as llm
    from google.genai import _api_client
    if getattr(llm, '_transport_retry_installed', False):
        return True
    recorder = Recorder(policy['output'], policy)
    if policy.get('harness_setup'):
        from _aideal_input_contract import prepare
        bindings = prepare(**policy['harness_setup'])
        recorder.metadata['harness_setup_version'] = 'aideal-output-setup-v1'
        recorder.event('harness_setup_checked', bindings=bindings,
                       note='Input bytes preserved; output directory created; prompt unchanged')
    os.environ['AIDEAL_GOOGLE_REQUEST_TIMEOUT_S'] = '600'
    os.environ['AIDEAL_GOOGLE_MAX_RETRIES'] = '1'
    original = llm.invoke_text
    @wraps(original)
    def invoke(spec, system, user):
        return recorder.invoke(original, spec, system, user)
    llm.invoke_text = invoke
    _api_client.BaseApiClient._request_once = sdk_wrapper(_api_client.BaseApiClient._request_once)
    llm._transport_retry_installed = True
    recorder.event('worker_enrolled', config=policy['config'], scope='future baseline provider retries only')
    print(f"[transport] {policy['version']} enabled: 600s x 1; outer 630s; "
          f"telemetry={policy['output']}", file=sys.stderr, flush=True)
    return True
