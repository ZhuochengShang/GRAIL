# RDPro before the remaining MDAnalysis stages

User scheduling instruction applied September 8 at 22:40 PDT.

Order: existing priority B2-1 work (currently tslearn) → RDPro v5 A2,
feedback, source-informed README repair and fresh B2 → new MDAnalysis stages.
RDPro's existing worker already checks only the three priority B2-1 summaries;
it has no MDAnalysis dependency. Its shared supplemental slot remains unchanged.

The MDAnalysis launch supervisor PID 49463 is deliberately held with SIGSTOP.
Its already-running A1 evaluation PID 49495 and README generation PID 49490
continue. No worker, checkpoint, measured config, original watchdog plan/state,
or input fingerprint was replaced. Only the supervisor PID is signalled, never
its process group. Its heartbeat will be old while held: this is an intentional
queue hold, not evidence that its two workers have died. Completion promotion,
new launches and watchdog retries resume when the hold ends.

`queue_priority.py` monitors the frozen RDPro watchdog identity and requires all
four jobs (`A2`, `feedback`, `repair`, `B2`) to succeed before sending SIGCONT
to the same MDAnalysis supervisor. Thus a completed README cannot start MDAnalysis
A2 ahead of RDPro. The separate MDAnalysis B2-1 waiter also cannot execute before
its own A2 exists. No measured source/prompt code or Gemini settings changed.

Registration: `rdpro_priority_20260908.policy.json`.
Resumable guard plan: `rdpro_priority_watchdog.yaml`.
Runtime status: workspace parent `AIDEAL_rdpro_priority_20260908/status.json`.
Activated guard supervisor PID 94044; guard worker PID 94047.
Both the guard lock and the watchdog lock reject duplicate launch attempts.
The guard rejects PID reuse and prerequisite-plan drift; unexpected errors hold
the queue and the guard supervisor retries. A graceful cancellation releases the
same MDAnalysis supervisor. An external kill/reboot requires normal process
reconciliation; do not treat a reused PID as the registered supervisor.

Validation: four offline tests passed (all-stage completion, plan drift,
PID reuse, supervisor-only signalling, preflight and automatic release).
Live check confirmed MD supervisor state `T`, both original MD workers alive
without `T`, and unchanged tslearn/RDPro worker PIDs. This is a scheduling
amendment; include the waiting interval in end-to-end timing, not API execution time.
