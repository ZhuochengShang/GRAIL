import json
import pytest
import yaml
from experiments.external.run_condition_watchdog import Supervisor


@pytest.mark.parametrize('payload', ['{truncated', '{}', '[]', '{"jobs":{}}'])
def test_corrupt_state_cannot_reset_to_pending(tmp_path, payload):
    plan = tmp_path / 'watchdog.yaml'
    plan.write_text(yaml.safe_dump({'jobs': [{'id': 'worker', 'cwd': str(tmp_path), 'command': ['test']}]}))
    state = plan.with_suffix('.state.json')
    state.write_text(payload)
    with pytest.raises((ValueError, json.JSONDecodeError)):
        Supervisor(plan)
    assert state.read_text() == payload
