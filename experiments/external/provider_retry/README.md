# Provider retries and execution reporting

This transport-only amendment is opt-in for four existing baseline retry workers.
It preserves model, temperature, prompt bytes, fixtures, zero snippet-fix budget,
and the 630-second outer invocation cap. It changes two transport settings:
one SDK attempt gets a 600-second request deadline, instead of two attempts with
300-second deadlines. This is a diagnosis/mitigation, not a proven cure for a
provider-side timeout. Requests that still fail remain explicit provider outcomes.

## Activation without restarting jobs

`enroll.py` installs a small, explicitly scoped Python `sitecustomize.py` bootstrap
on the existing worker PYTHONPATH. It applies only to the enrolled config's
`comprehension --resume --max-fix-rounds 0` commands. Current processes have already
imported their modules and are untouched. Existing supervisors naturally start
the next worker after the current invocation exits. No new supervisor or competing
API pipeline is needed. Generated API test processes are not enrolled.

The adapter uses the installed Google SDK's synchronous `_request_once` boundary;
SDK versions and adapter bytes are checked before activation. This private SDK
boundary must be reviewed when upgrading dependencies. No installed package is
modified. The implementation and paths are portable; `fcntl` requires POSIX.

## Policy and evidence

Each identical model/system/user request has a locked state file. Transient
errors impose a persisted exponential cooldown: 5, 10, 20, then at most 30 minutes,
with up to 10% jitter inside that cap. Reattempting during cooldown returns a
resumable provider outcome without sending a request. Successful generation
resets the streak. The request lock is held until completion; it does not expire
while a request might still be running. Existing shared Google request spacing
and supervisor ownership are retained. This is not an account-wide quota meter.

Separate per-process journals record UTC epoch start/end, request/prompt hashes,
API name, model, actual SDK timeout/server deadline, HTTP failure code, invocation
and SDK-attempt duration, and next eligible retry time. They never store prompt
text, response text, headers, URL queries or credentials. Interrupted start events
remain explicit missing-end records. A process exiting without a terminal event
does not establish success or release another still-live process's lock.

Native fingerprints predate this transport extension and do not encode it.
Therefore the adapter/policy hashes are a REQUIRED additional reporting dimension.
Do not present newly recovered provider cases as an unchanged-transport replication.
Native compilation/execution still determines pass/fail. Provider retries and
cooldown deferrals never become snippet-fix rounds or synthetic passes.

Run the offline checks with the existing experiment interpreter:

```sh
env PYTHONPATH=grail-agent/src:. python -m pytest -q experiments/external/provider_retry
```

`report.py` publishes explicit outcome labels and per-API timing. Old checkpoints
contain invocation duration but no start/end timestamp. Error-log timestamp gaps
are outcome-to-outcome intervals, not measured idle waits. New transport journals
provide actual provider start/end and eligible-retry times. Never reconstruct
unrecorded historical timings or claim that every target API was reached merely
because its generated test process ran.
