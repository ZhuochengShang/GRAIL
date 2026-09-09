import pytest
from .data import check_cells, historical_tables


def test_missing_is_not_zero_success():
    check_cells([{'n': 0, 'expected': 1032, 'statuses': {}}])
    with pytest.raises(ValueError):
        check_cells([{'n': 1032, 'expected': 1032, 'statuses': {'pass': 0}}])


def test_changed_historical_format_fails_closed():
    with pytest.raises(ValueError):
        historical_tables('| made-up B1 | 99/100 |')


def test_overfull_or_inconsistent_native_totals_rejected():
    for row in [{'n': 3, 'expected': 2, 'statuses': {'pass': 3}},
                {'n': 2, 'expected': 2, 'statuses': {'pass': 1}}]:
        with pytest.raises(ValueError):
            check_cells([row])
