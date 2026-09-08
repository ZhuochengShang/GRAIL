import signal
import time
import pytest
from aideal.provider_deadline import provider_deadline


@pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="POSIX wall deadline")
def test_wall_deadline_escapes_sdk_exception_retry_and_restores_handler():
    handler = signal.getsignal(signal.SIGALRM)
    started = time.monotonic()
    with pytest.raises(TimeoutError, match="total wall deadline"):
        with provider_deadline(0.04):
            # Simulate an SDK whose ordinary Exception retry loop would retry
            # a normal TimeoutError indefinitely.
            while True:
                try:
                    time.sleep(1)
                except Exception:
                    continue
    assert time.monotonic() - started < 0.8
    assert signal.getsignal(signal.SIGALRM) == handler
    assert signal.getitimer(signal.ITIMER_REAL)[0] == 0


def test_success_and_provider_errors_pass_through():
    with provider_deadline(1):
        pass
    with pytest.raises(ValueError, match="provider"):
        with provider_deadline(1):
            raise ValueError("provider")
