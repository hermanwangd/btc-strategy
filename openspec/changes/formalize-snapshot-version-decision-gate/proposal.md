## Why

The current workflow treats dirty or untracked source bytes as inadmissible and routes missing data through equivalent-source acquisition, but it has no approved way to use Herman Wang's exact hash-frozen local snapshot or to govern later hash drift. This change formalizes the approved direct-reference exception, two-tier admission, and snapshot-version decision Gate without applying any Multica configuration change.

## What Changes

- Register `USER_NOMINATED_SNAPSHOT_REFERENCE_V1` with its exact path, hashes, generation time, freeze, and cutoff.
- Add read-only, hash-first consumption and metadata-only publication rules for Gold, DXY, and DGS3MO; keep MVRV on existing HERM-130/HERM-124 evidence.
- Separate `RESULT_DISPOSITION` from `ADMISSION_TIER` and define `RESEARCH_ONLY` and `CANONICAL_ELIGIBLE`.
- Add deterministic snapshot-drift detection, one deduplicated approval event on HERM-118, an exact human-decision envelope, branch-scoped pause, dependency-aware invalidation, migration, and rollback.
- Replace the relevant Orchestrator and project-contract clauses while preserving independent Source Gate review and the strict serial lane.
- Preserve the comment-only watchdog, sealed holdout, immutable HERM-129/HERM-130 evidence, and all deployment/trading boundaries.

## Capabilities

### New Capabilities

- `snapshot-reference-governance`: Governs immutable local snapshot registration, admission tiers, drift decisions, artifact invalidation, errors, migration, and rollback.

### Modified Capabilities

None. The repository had no prior OpenSpec capability specifications.

## Impact

If separately approved and implemented, the change affects only `BTC Workflow Orchestrator.instructions` and the `BTC_Strategy_Multica` project description. It reuses HERM-118 and does not change Squad membership, agents, models, skills, runtimes, permissions, autopilots, watchdog behavior, source bytes, HERM-129/HERM-130, holdout state, or trading/deployment state.

This issue produces specification artifacts only. Applying these clauses requires a separate implementation review and authorization.
