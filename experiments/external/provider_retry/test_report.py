from .report import outcome, execution, provider_timing


def test_provider_failure_never_described_as_executed():
    row={'status':'fail','error_category':'llm-error','wall_s':600}
    assert outcome(row)=='Waiting for provider / retry'
    assert execution(row).startswith('No test code executed')


def test_compile_failure_is_not_runtime_failure():
    row={'status':'fail','error_category':'compile','execution_evidence':{'exit_code':1}}
    assert outcome(row)=='Compile failed'
    assert 'did not execute' in execution(row)


def test_process_success_does_not_certify_target_reached():
    row={'status':'pass','execution_evidence':{'exit_code':0}}
    assert 'not independently verified' in execution(row)


def test_retry_intervals_and_missing_end_are_not_invented():
    events=[{'event':'invocation_start','invocation_id':'a','epoch':100,'policy_sha256':'p'},
            {'event':'invocation_error','invocation_id':'a','epoch':700,'wall_s':600,'retry_after':1000},
            {'event':'invocation_start','invocation_id':'b','epoch':1050,'previous_end_epoch':700,'policy_sha256':'p'}]
    a,b=provider_timing(events)
    assert a['since_previous_provider_end_s'] is None
    assert a['provider_wall_s']==600
    assert b['since_previous_provider_end_s']==350
    assert b['end_epoch'] is None and b['provider_wall_s'] is None
    assert 'no end' in b['outcome']
