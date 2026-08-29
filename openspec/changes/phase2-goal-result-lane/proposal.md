## Why

The HERM-114 cohort has produced registration and build evidence but no independently validated pre-holdout CAGR/MDD scorecard. HERM-139–145 exposed late package, I/O-boundary, and envelope defects; HERM-160/HERM-162 then proved that prompt-only acceptance could falsely pass a load-before-filter path, omit a required fixture, and fail to wake the Orchestrator from three valid result events. The complete Phase-1 transaction was rolled back to exact prior hashes.

## What Changes

- Add one serial, autonomous `REGISTERED -> BUILD -> PREHOLDOUT_BACKTEST -> PERFORMANCE_GATE -> RECONCILE` lane for already approved, runnable candidates.
- Reuse HERM-118 (`BTC:DATA_READINESS:2017:CUTOFF_2026:V1`) as the sole shared prerequisite and preserve `SOURCE_ACQUISITION_CONTRACT_V2`.
- Require a versioned repository acceptance harness before any live clause is installed. The harness validates final bytes, adapter-level physical read bounds, typed single-envelope publication, identities, hashes, and load-before-filter failure using synthetic/schema fixtures only.
- Make terminal-result continuation an explicit trigger contract with stable event and transition keys, and retain Project Conveyor as comment-only recovery.
- Define bounded defect recovery, metrics, a compensated transaction, and a serial non-holdout replay.
- Keep portfolio parallelism disabled until a later activation Gate passes.

## Capabilities

### New Capabilities

- `goal-result-lane`: Produces independently reviewed pre-holdout CAGR/MDD scorecards from frozen registered candidates.
- `producer-acceptance-harness`: Enforces producer-local integrity and sealed-I/O constraints before publication.
- `result-event-continuation`: Wakes and deduplicates deterministic Orchestrator transitions.
- `workflow-observability`: Defines machine-observable throughput, latency, rework, wait, and safety metrics.

### Modified Capabilities

- `snapshot-reference-governance`: HERM-118 becomes a reusable admission prerequisite without changing its source, drift, tier, or holdout rules.

## Impact and authorization

This is a design and implementation plan only. It changes repository specification files, not strategy code, source bytes, Multica configuration, agent/Squad/autopilot settings, issue state machines, permissions, runtime, holdout state, or trading systems. A later approved compensated transaction would target only the exact objects and fields in `design.md`.

Recommendation: `APPROVE_PHASE2_TRANSACTION`, conditional on implementing and independently validating the repository harness before installing runtime clauses.
