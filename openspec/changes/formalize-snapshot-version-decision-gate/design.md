## Context

Authoritative records retrieved on 2026-08-27:

- `BTC Workflow Orchestrator` (`8cb3efc1-c123-4bf2-ab4a-af173e0570bc`) live `instructions` via `multica agent get`.
- `BTC_Strategy_Multica` (`b67b7971-cfeb-4067-992a-4119fe7f9cf9`) live `description` via `multica project get`.
- HERM-131 approval and constants.

The following replacements are proposed text only. They MUST NOT be applied under HERM-131.

## Current-to-proposed clauses: Orchestrator

### Current exact clause: `Required dirty-source decision gate`

```markdown
## Required dirty-source decision gate

A dirty source must trigger committed-baseline recovery before a BLOCKED handoff. When a recovery source is supplied, keep one recovery package and require its active child to:

1. Record source `git status --porcelain=v1`, branch, and `HEAD` without reset, clean, checkout, or overwrite.
2. Enumerate `refs/heads`, `refs/remotes`, and `refs/tags`; inspect reachable committed trees and relevant history for exact registered paths/hashes and V17 package components.
3. Choose in order: exact path/hash match, complete committed V17 package satisfying the frozen contract, then newest contract-satisfying committed candidate. Validate each selected file from `<commit>:<path>` and record ref/commit/blob/file SHA-256 before copying to the task worktree.
4. Continue the recovery from that committed baseline even when the checkout is dirty. Dirty working-tree bytes are never admissible by implication.

Only after the committed-baseline search plus authorized data/attachment/target search is exhausted may the child return BLOCKED. The BLOCKED evidence must list commands, refs/commits searched, exact missing paths, and owner/action; do not create a generic human data request or duplicate an active run.
```

### Proposed exact replacement: `Registered snapshot-reference decision gate`

```markdown
## Registered snapshot-reference decision gate

Generic dirty or untracked working-tree bytes MUST remain inadmissible. The sole exception is the exact immutable registration `USER_NOMINATED_SNAPSHOT_REFERENCE_V1`:

`REFERENCE_PATH=/Users/herman_mbp2023/Documents/btc_trading_strategy/outputs/btc_backtest_market_data_2016_2026_complete_v2`

`MANIFEST_SHA256=42ddcc7f0ebf1f842e27d7ac65be5ab980ed13f16710cfbd1212f0300e8cce0a`

`SHA256SUMS_SHA256=5601c62af3faa26d5f3127fa2213dddd0bf1b6eeb715f72ec40d26888d1e7ebc`

`BUNDLE_GENERATED_AT=2026-08-20T15:46:47.319260+00:00`

`DATA_FREEZE_AT=2026-08-26T14:56:00Z`
`CUTOFF_2026=2026-05-22`

The workflow MUST use this directory by direct read-only reference and MUST NOT copy, rename, modify, delete, chmod, or bind it as an in-place project resource. Every consumer MUST run `shasum -a 256 -c SHA256SUMS.txt` and verify both registered hashes before reading data. Gold, DXY, and DGS3MO MUST be read in place with `2017-01-01..2026-05-22` filtering at read time. Derived factor-ready artifacts MAY be written only in the project worktree and MUST record the absolute path, source hashes, row filters, availability lag, transformations, and output hashes. Publication MUST be metadata-only as `RESEARCH_REFERENCE_MANIFEST` or, after strict Source Gate evidence, `CANONICAL_REFERENCE_MANIFEST`. MVRV MUST reuse the latest readable HERM-130/HERM-124 evidence unless separately superseded.

If both frozen hashes match, continue to the independent Source Gate. Preserve `RESULT_DISPOSITION=PASS|REJECTED|BLOCKED|FAILED` and independently record `ADMISSION_TIER=RESEARCH_ONLY|CANONICAL_ELIGIBLE`. `RESEARCH_ONLY` requires hashes, schema, coverage, and `t close -> t+1` availability to pass but MUST NOT support final 2017-2026 qualification or CAGR/MDD claims. Only `CANONICAL_ELIGIBLE`, with strict point-in-time publication and revision evidence, MAY enter final qualification. A specific immutable version MAY receive source-quality `REJECTED`; hash drift MUST NOT.

If either hash differs, pause only dependent consumers. Observed unapproved bytes MAY be read only to calculate exact differences and MUST NOT enter factor construction, backtesting, qualification, or downstream calculations. Reuse HERM-118 and publish exactly one `SNAPSHOT_VERSION_APPROVAL_REQUIRED` event for the deterministic identity `SNAPSHOT_VERSION_APPROVAL_V1:<sha256(REFERENCE_PATH + "\n" + CURRENT_REFERENCE_ID + "\n" + OBSERVED_MANIFEST_SHA256 + "\n" + OBSERVED_SUMS_SHA256)>`, using exact strings and lowercase hashes. The identity is durable across unresolved and resolved states. Re-observing the tuple, including after `KEEP_CURRENT_SNAPSHOT`, MUST reuse that event and MUST NOT publish another.

The event MUST contain the complete HERM-131-approved envelope, including changed files, schema, coverage, source, cutoff, affected artifacts, and `SAFE_DEFAULT=KEEP_CURRENT_VERSION`. Continuation requires a matching `SNAPSHOT_VERSION_DECISION_V1` record on HERM-118 with decision, current reference ID, observed hashes, RFC3339 UTC timestamp, approval-event identity, and `DECISION_AUTHORITY=Herman Wang`. The comment author MUST resolve to workspace member ID `22a02dd4-c3de-44ce-b702-2311cba7aefa` and user ID `87261ec4-8bcd-4355-8e50-57514c7e1345`; an agent-authored or other-member envelope carrying the authority string is `DECISION_RECORD_ERROR`.

Immediately before `ADOPT_NEW_SNAPSHOT`, recompute both observed hashes. The decision authorizes only its exact tuple. A different current tuple MUST supersede the old event for execution, MUST NOT be adopted under the old decision, and MUST create or reuse one event for its own identity. A matching `ADOPT_NEW_SNAPSHOT` MUST register a new immutable version, preserve V1 permanently, rerun the Source Gate, and rebuild or invalidate only artifacts proven to depend on changed bytes or semantics. `KEEP_CURRENT_SNAPSHOT` MUST keep V1 authoritative and observed bytes inadmissible; if V1 is unavailable, only dependent work enters `WAITING_FOR_V1_RESTORE` until V1 validates or a genuinely different tuple creates one distinct event. Unrelated candidates MUST continue.

An unreadable local path is `LOCAL_REFERENCE_UNAVAILABLE`; an authorized artifact handoff returning `HTTP 403` is `ARTIFACT_HANDOFF_ERROR`. Neither is source-quality `REJECTED` or an external reacquisition trigger. Route internal access/handoff repair. HERM-129 and HERM-130 MUST remain immutable. Project Conveyor MUST remain comment-only and recovery-only.
```

### Current exact clause: equivalent-only serial state machine

```markdown
### Equivalent-only source acquisition and backfill state machine (`SOURCE_ACQUISITION_CONTRACT_V1`)

This section is authoritative for missing or incomplete source-data dependencies and supersedes conflicting source-acquisition wording. It does not relax sealed-holdout, candidate evaluation, promotion, deployment, capital, paper/live integration, or trading boundaries.

Run these states serially, with one active functional child or Gate child at a time:

`SOURCE_CONTRACT → ACQUIRE_TO_CANDIDATE → SOURCE_GATE → CANONICAL_PUBLISH → FACTOR_READY_BUILD → READINESS_GATE`
```

The remainder of the current clause defines HERM-118 reuse; HERM-119 immutability; source contracts; prioritized equivalent-source acquisition; Source Gate; canonical publication; factor-ready build; readiness Gate; four-category human approval; external waiting; watchdog timing; and duplicate protection. It is quoted in full by the authoritative record and is replaced as one section by the following exact text.

### Proposed exact replacement: direct-reference and fallback state machine

```markdown
### Direct-reference and equivalent-only source state machine (`SOURCE_ACQUISITION_CONTRACT_V2`)

This section is authoritative for missing, incomplete, or user-nominated snapshot source dependencies. It preserves sealed-holdout, candidate-evaluation, promotion, deployment, capital, paper/live, and trading boundaries.

For the registered V1 local bundle, execute serially:

`SOURCE_CONTRACT → REGISTER_DIRECT_REFERENCE → VERIFY_FROZEN_HASHES → SOURCE_GATE → RESEARCH_REFERENCE_MANIFEST|CANONICAL_REFERENCE_MANIFEST → FACTOR_READY_BUILD → READINESS_GATE`

`REGISTER_DIRECT_REFERENCE` MUST create metadata only and MUST NOT copy source bytes. `VERIFY_FROZEN_HASHES` MUST validate `SHA256SUMS.txt` and both registered hashes before data access. Hash match proceeds to the independent Source Gate. Hash drift branches to `SNAPSHOT_VERSION_DECISION`; `KEEP_CURRENT_SNAPSHOT` returns to `VERIFY_FROZEN_HASHES` when V1 is readable or `WAITING_FOR_V1_RESTORE` otherwise, without duplicating the durable event for an identical tuple. Immediately before `ADOPT_NEW_SNAPSHOT`, recompute both observed hashes; only an exact decision-tuple match may register a new immutable version and return through `SOURCE_GATE`, while a changed tuple supersedes the old event for execution and creates or reuses its own event. Decision comments MUST be authored by the authorized Herman Wang member/user IDs, not merely carry the authority string. Direct reference MUST NOT bypass Source Gate.

The Source Gate MUST independently record `RESULT_DISPOSITION` and `ADMISSION_TIER`. `RESEARCH_ONLY` MAY publish only `RESEARCH_REFERENCE_MANIFEST`; `CANONICAL_ELIGIBLE` MAY publish `CANONICAL_REFERENCE_MANIFEST` and enter final qualification only after all remaining gates. Publication is metadata-only. Gold, DXY, and DGS3MO are read in place; MVRV remains governed by the latest readable HERM-130/HERM-124 evidence.

If the registered reference is unavailable, classify `LOCAL_REFERENCE_UNAVAILABLE` and route internal runtime-access repair. If an authorized handoff returns `HTTP 403`, classify `ARTIFACT_HANDOFF_ERROR` and route internal artifact-handoff repair. Neither error is source-quality `REJECTED` or external reacquisition. The prior Stooq `EXTERNAL_WAIT` is superseded for Gold/DXY/DGS3MO while the local reference is readable and validates.

If no approved immutable direct reference is usable after internal repair, the existing equivalent-only fallback remains serial:

`SOURCE_CONTRACT → ACQUIRE_TO_CANDIDATE → SOURCE_GATE → CANONICAL_PUBLISH → FACTOR_READY_BUILD → READINESS_GATE`

The fallback MUST retain frozen semantics, one unique source at a time, bounded retries, segmented fetches, deterministic append/deduplication, UTC normalization, schema/provenance/coverage/release-lag/row-count/SHA-256 evidence, atomic writes, rollback on regression, independent Source Gate, one same-source Advanced retry after reproducible Basic failure, proxy quarantine, and the existing four approval categories `CREDENTIALS|PROVIDER_ACCESS|COST|LICENSE`. It MUST NOT be entered solely because registered hashes drift, the local path is unreadable, or a handoff returns `HTTP 403`.

Reuse HERM-118 for `DEPENDENCY_ID=BTC:DATA_READINESS:2017:CUTOFF_2026:V1`; do not create a duplicate parent. Preserve HERM-129 and HERM-130 as immutable evidence. Protect all non-terminal work from duplicate dispatch. Pause blockers only at their true branch scope and keep unrelated candidates active. Project Conveyor remains comment-only and recovery-only.
```

## Current-to-proposed clauses: project contract

### Current exact clause: `13A. Dependency-resolution lane`

```markdown
## 13A. Dependency-resolution lane and approved one-time boundary policy

This section is an authoritative amendment to the HERM-114 Phase-1 fallback. It supersedes any wording that maps every “no admissible candidate” state directly to registration-only work.

When a registered candidate cannot run:

1. reconcile its current evidence;
2. classify its blocker and scope;
3. create or reuse one stable dependency-resolution parent when an existing lane can produce the missing artifact;
4. continue unrelated candidates;
5. replenish registrations only when the unconsumed registered queue is genuinely empty.

For the current 2017–2026 blocker, create one Squad-owned data-readiness parent under the active project-goal frontier with stable identity `BTC:DATA_READINESS:2017:CUTOFF_2026:V1`.

The Orchestrator routes its stages through existing members only:

1. `BTC Basic Market Evidence Analyst`: identify authorized sources; determine `CUTOFF_2026` using the approved latest-common-admissible-date rule; produce raw-byte coverage, release-lag, provenance, schema, row-count, and SHA-256 manifest evidence.
2. `BTC Basic Backtest Engineer`: after the raw manifest and candidate input contract are frozen, build the deterministic HERM-77-compatible factor-ready object and record transformation, environment, command, schema, row-count, and SHA-256 identities. This is `DATA_PREPARATION`, not candidate evaluation.
3. `BTC Validation & Risk Gate`: independently verify the completed data-readiness package. A Gate `PASS` validates readiness only; it does not qualify a strategy or authorize deployment, capital, paper/live integration, or trading.

The 2024-through-`CUTOFF_2026` bytes remain sealed from candidate-conditioned performance inspection during data preparation. Exactly one project-level unseal is authorized for one nominated finalist after frozen rules and implementation, completed development/validation/walk-forward checks, and an independent pre-holdout Gate `PASS`. No retuning is allowed after unseal. Another attempt requires explicit human approval and a versioned boundary contract.

Any registration package dispatched before this amendment, including HERM-115 and HERM-117, is grandfathered. Do not cancel, rerun, or duplicate it. If non-terminal, let it finish once; if terminal, reconcile it once and treat any validated `PASS` registration as unconsumed inventory. Do not create another equivalent registration-only child while any grandfathered package is non-terminal or that unconsumed registration exists. HERM-112/HERM-113 remain immutable; use a versioned successor after data readiness passes.

Project Conveyor remains comment-only and recovery-only. It may wake the Orchestrator after a missed transition but must never create, assign, or dispatch this lane.
```

### Proposed exact replacement: `13A`

```markdown
## 13A. Dependency-resolution lane, immutable snapshot reference, and approved one-time boundary policy

When a registered candidate cannot run, the Orchestrator MUST reconcile evidence, classify blocker class and scope, reuse one stable dependency-resolution parent, continue unrelated candidates, and replenish registration only when unconsumed inventory is empty. For the 2017-2026 dependency it MUST reuse HERM-118 with `DEPENDENCY_ID=BTC:DATA_READINESS:2017:CUTOFF_2026:V1`.

`USER_NOMINATED_SNAPSHOT_REFERENCE_V1` MUST register the exact HERM-131 path, manifest hash, sums hash, bundle time, `DATA_FREEZE_AT=2026-08-26T14:56:00Z`, and `CUTOFF_2026=2026-05-22`. It MUST be a direct read-only, metadata-published exception limited to those exact identifiers. Every consumer MUST validate `shasum -a 256 -c SHA256SUMS.txt` before reading. No source copy or mutation is permitted.

The Orchestrator MUST route the direct-reference states through existing members and the independent Source Gate under `SOURCE_ACQUISITION_CONTRACT_V2`. Admission MUST be independent of disposition: `RESEARCH_ONLY` MAY support caveated research but MUST NOT support final qualification or CAGR/MDD claims; only `CANONICAL_ELIGIBLE` MAY proceed toward final qualification.

Hash drift MUST pause only dependent consumers and MUST enter the deduplicated HERM-118 snapshot-version decision Gate. Approval identity MUST persist after resolution. `KEEP_CURRENT_SNAPSHOT` MUST never duplicate an event for the same tuple and MUST use `WAITING_FOR_V1_RESTORE` when V1 is unavailable. Immediately before `ADOPT_NEW_SNAPSHOT`, hashes MUST be recomputed and only the exact authorized tuple may be adopted; a changed tuple requires its own event. Decision authority MUST be verified against Herman Wang's authorized workspace member and user IDs. V1, HERM-129, and HERM-130 evidence MUST remain immutable. Access and handoff errors MUST route internal repair, not source rejection or external reacquisition.

The 2024-through-`CUTOFF_2026` bytes MUST remain sealed from candidate-conditioned performance inspection during data preparation. Exactly one project-level unseal remains authorized for one nominated finalist only after frozen rules and implementation, completed development/validation/walk-forward checks, and independent pre-holdout Gate `PASS`. No retuning is allowed after unseal; another attempt requires explicit human approval and a versioned boundary contract.

Existing grandfathered registration and immutable HERM-112/HERM-113 rules remain unchanged. Project Conveyor MUST remain comment-only and recovery-only and MUST NOT create, assign, or dispatch this lane.
```

### Current exact clause: `13B` strict flow

```markdown
The Orchestrator MUST execute this lane serially:

`SOURCE_CONTRACT → ACQUIRE_TO_CANDIDATE → SOURCE_GATE → CANONICAL_PUBLISH → FACTOR_READY_BUILD → READINESS_GATE`
```

The full current `13B` (retrieved from the project description) additionally mandates HERM-118 reuse, HERM-119 immutability, frozen source contract, equivalent-only acquisition, independent Source Gate, canonical publication, factor-ready build, readiness Gate, four-category human approval, and rollback.

### Proposed exact replacement: project `13B`

The project description MUST replace all of current `13B` with the exact Orchestrator `SOURCE_ACQUISITION_CONTRACT_V2` text above, plus the following project-only acceptance paragraph:

```markdown
### Acceptance and rollback

Implementation is accepted only when exactly the approved Orchestrator instructions and project description clauses change; Squad membership, Squad instructions, agents, models, skills, runtimes, permissions, autopilots, worker/Gate prompts, watchdog boundaries, source bytes, and HERM-129/HERM-130 remain unchanged. HERM-118 remains the sole dependency parent. Tests MUST demonstrate the ten HERM-131 acceptance scenarios plus persistent deduplication after `KEEP_CURRENT_SNAPSHOT`, freshness before adoption, and real decision-author verification. Rollback MUST restore exact pre-change text while preserving every version, approval, decision, Gate, manifest, and lineage record produced under the contract.
```

## Decisions and rationale

1. **Hash-first direct reference.** This is the smallest exception that makes the nominated bundle actionable without generalizing trust to dirty bytes.
2. **Disposition and tier are orthogonal.** Source quality remains independently rejectable; research usefulness does not imply qualification eligibility.
3. **Event identity uses four exact fields.** It is deterministic, stable across retries, and distinct for a new observed tuple.
4. **Branch-scoped pause and lineage invalidation.** This avoids freezing unrelated research or rebuilding content-addressed artifacts unaffected by changed bytes/semantics.
5. **V2 reruns Source Gate.** Human adoption approves the immutable version, not its source quality or canonical eligibility.

## State and event model

States are `SOURCE_CONTRACT`, `REGISTER_DIRECT_REFERENCE`, `VERIFY_FROZEN_HASHES`, `SNAPSHOT_VERSION_DECISION`, `SOURCE_GATE`, `RESEARCH_REFERENCE_MANIFEST`, `CANONICAL_REFERENCE_MANIFEST`, `FACTOR_READY_BUILD`, and `READINESS_GATE`. Terminal/error conditions are `LOCAL_REFERENCE_UNAVAILABLE`, `ARTIFACT_HANDOFF_ERROR`, `DECISION_RECORD_ERROR`, and `INVALIDATION_REVIEW_REQUIRED`; these do not change `RESULT_DISPOSITION` unless a Gate separately evaluates source quality.

The approval and decision envelopes and their validations are normative in the capability spec. HERM-118 is the sole event/decision ledger for this dependency.

## Migration

1. Capture exact pre-change Orchestrator instructions and project description for rollback.
2. Install the proposed replacement clauses only after separate approval.
3. Register V1 metadata on HERM-118 without reading, copying, or transforming source bytes.
4. Reconcile existing HERM-118 work; do not duplicate non-terminal tasks and do not alter HERM-129/HERM-130.
5. Resume at `VERIFY_FROZEN_HASHES`; retain equivalent-only acquisition only as the bounded fallback defined in V2.

## Rollback

Restore the captured text fields exactly. Do not erase evidence created under V2. Disable new direct-reference starts; require compatibility review before reusing artifacts produced under V2.

## Risks

- An in-place path may cease to expose V1 bytes. The safe default keeps V1 authoritative and pauses only dependents.
- Incomplete lineage can over-invalidate. `INVALIDATION_REVIEW_REQUIRED` chooses safety over silent reuse.
- A human response may be malformed or attached to the wrong event. Exact identity/hash matching prevents continuation.
- Research-only results may be mistaken for qualification. Mandatory tier labeling and claim prohibition make that misuse testable.
