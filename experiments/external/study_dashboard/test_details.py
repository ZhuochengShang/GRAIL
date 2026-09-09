from .details_data import derived, saved_snippet


def row(name, a2=None, b2=None, category=None):
    return {'api': name, 'native': {
        'A2': {'metric': {'status': a2}},
        'B2': {'metric': {'status': b2, 'error_category': category}}}}


def test_pending_and_provider_errors_do_not_become_regressions():
    data = derived([row('pending', 'pass'), row('provider', 'pass', 'fail', 'llm-error'),
                    row('gain', 'fail', 'pass'), row('lost', 'pass', 'fail')], None)
    assert data['paired_A2_B2_outcomes'] == 2
    assert data['A2_fail_B2_pass'] == ['gain']
    assert data['A2_pass_B2_fail'] == ['lost']


def test_repair_validation_is_separate_from_fresh_test():
    doc = {'apis': {'api': {'status': 'doc-fixed', 'doc_rounds': [
        {'round': 0}, {'round': 1, 'retry_status': 'pass'}]}}}
    data = derived([row('api', 'fail', 'fail')], doc)
    assert data['document_round_records'] == 2
    assert data['validation_outcomes'] == {'no validation outcome recorded': 1, 'pass': 1}
    assert data['retained_entry_B2_fail'] == ['api']
    assert not data['A2_pass_B2_fail']


def test_resumed_status_text_is_not_a_retained_snippet():
    assert saved_snippet({'details': {'api': 'resumed: pass'}}, 'api') is None
    assert saved_snippet({'details': {'api': {'code': 'real code'}}}, 'api') == 'real code'
