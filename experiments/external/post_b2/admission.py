"""One shared supplemental worker slot, reserving capacity for live priority jobs."""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import time

from .evidence import REPOSITORIES


def native_reservation(upstream):
    """Conservative envelope: two native callers/repo, one after its B2 ends.

    After B2 the original driver runs A1 OR residual source retries, sequentially.
    Reserving those slots also covers future native launches without a racy PID
    count. This bounds this three-repository study, not unrelated account users.
    """
    total = 0
    for repo in REPOSITORIES:
        try:
            jobs = json.loads((Path(upstream) / repo / 'b2_watchdog.state.json').read_text())['jobs']
            finished = bool(jobs) and all(row.get('status') == 'succeeded' for row in jobs.values())
        except (OSError, ValueError, KeyError):
            finished = False
        total += 1 if finished else 2
    return total


@contextmanager
def slot(upstream, purpose):
    # This is a configured local concurrency cap, not a claimed Gemini quota.
    path = Path(os.environ.get('AIDEAL_GOOGLE_RECOVERY_ADMISSION_LOCK',
                               '/tmp/aideal_google_recovery_admission.lock'))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            reserved = native_reservation(upstream)
            if reserved + 1 > 6:
                yield False
                return
            if (not os.environ.get('AIDEAL_GOOGLE_RATE_STATE')
                    or float(os.environ.get('AIDEAL_GOOGLE_MIN_INTERVAL_S', '0')) < 3):
                raise ValueError('existing shared Google request-start gate is required')
            lock.seek(0)
            lock.truncate()
            json.dump({'pid': os.getpid(), 'purpose': purpose, 'started_epoch': time.time(),
                       'native_reserved': reserved, 'supplemental_slots': 1,
                       'local_study_max_callers': 6}, lock)
            lock.flush()
            yield True
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
