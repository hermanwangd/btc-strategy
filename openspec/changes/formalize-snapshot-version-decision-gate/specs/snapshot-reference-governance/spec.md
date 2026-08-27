## ADDED Requirements

### Requirement: immutable direct-reference registration

The workflow MUST register exactly this source contract as `USER_NOMINATED_SNAPSHOT_REFERENCE_V1`:

```text
REFERENCE_ID=USER_NOMINATED_SNAPSHOT_REFERENCE_V1
REFERENCE_PATH=/Users/herman_mbp2023/Documents/btc_trading_strategy/outputs/btc_backtest_market_data_2016_2026_complete_v2
MANIFEST_SHA256=42ddcc7f0ebf1f842e27d7ac65be5ab980ed13f16710cfbd1212f0300e8cce0a
SHA256SUMS_SHA256=5601c62af3faa26d5f3127fa2213dddd0bf1b6eeb715f72ec40d26888d1e7ebc
BUNDLE_GENERATED_AT=2026-08-20T15:46:47.319260+00:00
DATA_FREEZE_AT=2026-08-26T14:56:00Z
CUTOFF_2026=2026-05-22
```

The reference MUST be direct and read-only. The workflow MUST NOT copy, rename, modify, delete, chmod, or bind the source directory as an in-place project resource. Every consumer MUST execute `shasum -a 256 -c SHA256SUMS.txt` from the referenced package and verify both registered frozen hashes before reading data.

This explicit user-nominated, hash-verified reference MUST be the sole exception to the generic dirty/untracked-source prohibition. The exception MUST apply only to the exact registered path and hashes and MUST NOT imply that any other dirty or untracked bytes are admissible.

Gold, DXY, and DGS3MO MUST be read in place and filtered to `2017-01-01..2026-05-22` at read time. Factor-ready derived artifacts MAY be written only in the project worktree and MUST record absolute source path, source hashes, row filters, availability lag, transformations, and output hashes. Publication MUST be metadata-only: `RESEARCH_REFERENCE_MANIFEST` for caveated research and `CANONICAL_REFERENCE_MANIFEST` only after strict evidence passes. Publication MUST NOT copy source bytes.

MVRV MUST remain outside the local bundle and MUST reuse the latest readable evidence from HERM-130/HERM-124 unless a separately approved source decision supersedes it.

#### Scenario: frozen hashes match

- **Given** the registered path is readable and both package hashes match V1
- **When** the consumer validates `SHA256SUMS.txt` before any data read
- **Then** validation succeeds and the branch continues without human approval, subject to the independent Source Gate and admission-tier rules.

#### Scenario: prohibited source mutation

- **Given** the V1 reference is registered
- **When** any workflow task consumes or publishes it
- **Then** no source copy, rename, modification, deletion, chmod, or in-place project-resource bind occurs.

### Requirement: independent disposition and admission tier

The workflow MUST retain `RESULT_DISPOSITION=PASS|REJECTED|BLOCKED|FAILED` and MUST record an independent `ADMISSION_TIER=RESEARCH_ONLY|CANONICAL_ELIGIBLE` for a Source Gate result.

`ADMISSION_TIER=RESEARCH_ONLY` MUST require passing hashes, schema, coverage, and `t close -> t+1` availability. Point-in-time publication or revision evidence MAY remain uncertain. Research-factor work MAY proceed, but final 2017–2026 qualification and net CAGR/MDD claims MUST NOT use this tier.

`ADMISSION_TIER=CANONICAL_ELIGIBLE` MUST require strict point-in-time publication and revision evidence to pass. Only this tier MAY enter final qualification.

A Source Gate MAY return source-quality `RESULT_DISPOSITION=REJECTED` after evaluating a specific immutable snapshot version. Snapshot-version drift itself MUST be governance state and MUST NOT be classified as source-quality `REJECTED`.

#### Scenario: research-only admission

- **Given** hashes, schema, coverage, and `t close -> t+1` availability pass but strict publication or revision evidence does not pass
- **When** the Source Gate records its result
- **Then** research work may continue under `RESEARCH_ONLY`, while final CAGR/MDD qualification remains blocked.

#### Scenario: canonical admission

- **Given** strict point-in-time and revision evidence passes for the immutable version
- **When** the Source Gate records `CANONICAL_ELIGIBLE`
- **Then** final qualification is allowed to continue through the remaining independent gates and frozen evaluation protocol.

### Requirement: snapshot-version drift detection and isolation

Before every consumption, the workflow MUST compare the observed manifest and sums hashes with the registered immutable version. If either hash differs, it MUST pause only consumers of that snapshot. Unrelated candidates and strategy families MUST continue.

The workflow MAY read observed unapproved bytes only to calculate and report file-hash, schema, coverage, source, and cutoff differences. It MUST NOT use observed unapproved bytes for factor construction, backtesting, qualification, or any downstream calculation.

#### Scenario: a frozen hash differs

- **Given** either observed hash differs from V1
- **When** pre-read validation detects drift
- **Then** no observed bytes enter calculations, only affected consumers pause, and the approval-event requirement is activated.

### Requirement: deterministic approval event

The Orchestrator MUST publish exactly one unresolved top-level event on HERM-118 using this envelope:

```text
SNAPSHOT_VERSION_APPROVAL_REQUIRED
REFERENCE_PATH=<exact path>
CURRENT_REFERENCE_ID=<V1>
CURRENT_MANIFEST_SHA256=<old hash>
OBSERVED_MANIFEST_SHA256=<new hash>
CURRENT_SUMS_SHA256=<old hash>
OBSERVED_SUMS_SHA256=<new hash>
CHANGED_FILES=<old/new hashes>
SCHEMA_DIFF=<exact diff or NONE>
COVERAGE_DIFF=<exact diff or NONE>
SOURCE_DIFF=<exact diff or NONE>
CUTOFF_IMPACT=<exact impact or NONE>
AFFECTED_ARTIFACTS=<identities>
SAFE_DEFAULT=KEEP_CURRENT_VERSION
END_SNAPSHOT_VERSION_APPROVAL_REQUIRED
```

The deterministic approval identity MUST be:

```text
SNAPSHOT_VERSION_APPROVAL_V1:<sha256(UTF-8(
  REFERENCE_PATH + "\n" +
  CURRENT_REFERENCE_ID + "\n" +
  OBSERVED_MANIFEST_SHA256 + "\n" +
  OBSERVED_SUMS_SHA256
))>
```

All four inputs MUST use their exact envelope strings without whitespace normalization; hashes MUST be lowercase hexadecimal. The approval identity MUST remain durable across unresolved and resolved states. Re-observing the same tuple MUST reuse the existing event and MUST NOT publish another, including after a matching `KEEP_CURRENT_SNAPSHOT` decision. A different observed tuple MAY create one distinct event.

#### Scenario: repeated identical drift

- **Given** an unresolved event exists for the same four-field tuple
- **When** the same drift is observed again
- **Then** the existing event is reused and no duplicate is published.

#### Scenario: distinct drift tuple

- **Given** an event exists for one observed tuple
- **When** either observed hash differs from that tuple
- **Then** one distinct approval event is permitted under its distinct deterministic identity.

#### Scenario: repeated identical drift after keep-current decision

- **Given** an event for the same four-field tuple has a matching `KEEP_CURRENT_SNAPSHOT` decision
- **When** the identical tuple is observed again
- **Then** the durable event and decision are reused, no new approval event is published, and the branch enters or remains `WAITING_FOR_V1_RESTORE` when V1 bytes are unavailable.

### Requirement: durable human decision

Snapshot drift MUST stop only the affected branch for Herman Wang. Before continuation, the decision MUST be durably recorded on HERM-118 using exactly:

```text
SNAPSHOT_VERSION_DECISION_V1
DECISION=<ADOPT_NEW_SNAPSHOT|KEEP_CURRENT_SNAPSHOT>
CURRENT_REFERENCE_ID=<V1>
OBSERVED_MANIFEST_SHA256=<64 lowercase hex>
OBSERVED_SUMS_SHA256=<64 lowercase hex>
DECISION_AUTHORITY=Herman Wang
DECIDED_AT=<RFC3339 UTC timestamp>
APPROVAL_EVENT_ID=<SNAPSHOT_VERSION_APPROVAL_V1 identity>
END_SNAPSHOT_VERSION_DECISION_V1
```

The Orchestrator MUST verify that the response hashes and event identity match the applicable event, that `DECISION_AUTHORITY=Herman Wang`, and that the decision comment author resolves to workspace member ID `22a02dd4-c3de-44ce-b702-2311cba7aefa` and user ID `87261ec4-8bcd-4355-8e50-57514c7e1345`. The authority string is necessary but not sufficient. An agent-authored or other-member comment carrying that string MUST be classified `DECISION_RECORD_ERROR`. Malformed, mismatched, duplicated, or unauthorized responses MUST also be classified `DECISION_RECORD_ERROR`, MUST NOT continue the affected branch, and SHOULD receive one correction request on the same HERM-118 thread.

This Gate is a material data-contract decision and is an authorized stop-for-Herman trigger.

#### Scenario: authorized matching decision

- **Given** one unresolved approval event and a decision envelope whose identity and observed hashes match it
- **When** Herman Wang posts `DECISION_AUTHORITY=Herman Wang` on HERM-118 and the comment author resolves to both authorized IDs
- **Then** the Orchestrator may execute exactly the selected continuation transition.

#### Scenario: invalid decision record

- **Given** a decision envelope is malformed, mismatched, duplicated, or unauthorized
- **When** the Orchestrator validates it
- **Then** the affected branch remains stopped with `DECISION_RECORD_ERROR` and at most one correction request is made on the same thread.

#### Scenario: spoofed decision authority

- **Given** an agent or non-Herman member posts a matching envelope with `DECISION_AUTHORITY=Herman Wang`
- **When** the Orchestrator resolves the real comment author
- **Then** the affected branch remains stopped with `DECISION_RECORD_ERROR` and the envelope authorizes no transition.

### Requirement: adopt-new-snapshot transition

For `ADOPT_NEW_SNAPSHOT`, immediately before adoption the workflow MUST recompute the observed manifest and sums hashes. A decision MUST authorize only its exact observed tuple. If the path exposes a different tuple, the old event and decision MUST be marked superseded for execution purposes, MUST NOT authorize the newly observed bytes, and the workflow MUST create or reuse exactly one event for the new deterministic identity. Only after the fresh tuple matches the authorized decision MUST the workflow register a new immutable monotonically versioned reference (V2 after V1), retain V1 evidence permanently, bind the decision identity to the new registration, and rerun the independent Source Gate before publication or downstream use.

The workflow MUST invalidate or rebuild only artifacts whose recorded lineage proves dependency on changed bytes or changed semantics. Content-addressed artifacts with unchanged complete transitive inputs and semantics MUST remain valid. An artifact with missing or ambiguous lineage MUST be conservatively marked `INVALIDATION_REVIEW_REQUIRED` and MUST NOT enter final qualification until resolved.

#### Scenario: adopt a new snapshot

- **Given** a matching authorized `ADOPT_NEW_SNAPSHOT` response exists
- **When** the Orchestrator reconciles it
- **Then** it registers V2, retains V1 evidence, reruns Source Gate admission for V2, and rebuilds or invalidates only affected downstream artifacts.

#### Scenario: stale adopt decision

- **Given** an authorized `ADOPT_NEW_SNAPSHOT` decision exists for one observed tuple
- **When** the immediately recomputed manifest or sums hash exposes a different tuple
- **Then** the old event is superseded for execution, no newly observed bytes are adopted, and the workflow creates or reuses the single event for the new deterministic identity.

### Requirement: keep-current-snapshot transition

For `KEEP_CURRENT_SNAPSHOT`, V1 MUST remain authoritative and observed bytes MUST remain inadmissible. If the exact V1 bytes remain readable, affected work MAY resume using V1 after hash validation. If V1 bytes are not readable at the registered reference, only dependent work MUST enter `WAITING_FOR_V1_RESTORE` until V1 validates or a genuinely different observed tuple creates one distinct event; unrelated work MUST continue. Re-observing the kept tuple MUST NOT create another approval event.

#### Scenario: keep current while V1 is readable

- **Given** a matching authorized `KEEP_CURRENT_SNAPSHOT` response and readable V1 bytes
- **When** the affected branch resumes
- **Then** it uses only validated V1 bytes and does not use observed unapproved bytes.

#### Scenario: keep current while V1 is unavailable

- **Given** a matching authorized `KEEP_CURRENT_SNAPSHOT` response but V1 bytes are unavailable
- **When** the branch attempts to resume
- **Then** only V1-dependent work waits for restoration or a later decision, while unrelated work continues.

### Requirement: access and handoff error classification

An unreadable local path MUST be classified `LOCAL_REFERENCE_UNAVAILABLE`. An `HTTP 403` encountered while retrieving an already-authorized artifact handoff MUST be classified `ARTIFACT_HANDOFF_ERROR`. Neither condition MUST be classified source-quality `REJECTED`, and neither MUST trigger external source reacquisition.

The next action MUST be internal runtime-access or artifact-handoff repair. The prior Stooq `EXTERNAL_WAIT` MUST be superseded for Gold, DXY, and DGS3MO whenever the approved local reference is available and validates.

#### Scenario: local reference or handoff unavailable

- **Given** the local path is unreadable or an authorized handoff returns `HTTP 403`
- **When** the workflow classifies the failure
- **Then** it records the corresponding access/handoff error and routes internal repair, without `REJECTED` or external reacquisition.

### Requirement: migration and immutable evidence

Implementation MUST reuse HERM-118 as `DEPENDENCY_ID=BTC:DATA_READINESS:2017:CUTOFF_2026:V1` and MUST NOT create a duplicate dependency parent. HERM-129 and HERM-130 MUST remain immutable and MUST NOT be rerun, rewritten, or erased. Existing non-terminal work MUST NOT be duplicated. Other candidate families MUST continue unless they depend on the unresolved snapshot state.

The strict lane MUST become:

```text
SOURCE_CONTRACT
→ REGISTER_DIRECT_REFERENCE
→ VERIFY_FROZEN_HASHES
→ SOURCE_GATE
→ RESEARCH_REFERENCE_MANIFEST when RESEARCH_ONLY
  OR CANONICAL_REFERENCE_MANIFEST when CANONICAL_ELIGIBLE
→ FACTOR_READY_BUILD
→ READINESS_GATE
```

On hash drift, `VERIFY_FROZEN_HASHES` MUST branch to `SNAPSHOT_VERSION_DECISION`, then return to `VERIFY_FROZEN_HASHES` for `KEEP_CURRENT_SNAPSHOT` or to `REGISTER_DIRECT_REFERENCE → SOURCE_GATE` for `ADOPT_NEW_SNAPSHOT`. The direct-reference path MUST NOT bypass the independent Source Gate.

#### Scenario: migration preserves workflow boundaries

- **Given** the new contract is separately approved for implementation
- **When** it is installed
- **Then** HERM-118 is reused, HERM-129/HERM-130 remain unchanged, no source bytes are copied, and the independent Source Gate remains mandatory.

### Requirement: rollback

Rollback MUST restore the exact pre-change `BTC Workflow Orchestrator.instructions` and project `description` values. It MUST NOT delete any registered reference version, approval event, decision record, Source Gate result, manifest, or lineage evidence created while the contract was active. After rollback, no new direct-reference consumption MAY start; already produced artifacts MUST retain their identities and MUST require explicit compatibility review before reuse.

#### Scenario: contract rollback

- **Given** the change was implemented and rollback is authorized
- **When** the exact prior text values are restored
- **Then** runtime behavior returns to the prior acquisition contract while all version and decision evidence remains auditable.

### Requirement: invariant boundaries

This capability MUST NOT authorize holdout unseal, candidate qualification without all existing gates, promotion, deployment, capital action, paper/live integration, or trading. The Project Conveyor MUST remain comment-only and recovery-only. The workflow MUST preserve the project objective of independently validating at least one candidate with net `CAGR > 80%` and absolute `MDD < 50%` over the frozen 2017-through-2026 evaluation window.

#### Scenario: no forbidden side effect

- **Given** any path through this state machine
- **When** it completes or blocks
- **Then** no duplicate HERM-118 parent, source mutation, HERM-129/HERM-130 rewrite, unrelated-candidate pause, holdout unseal, deployment, capital action, paper/live integration, or trading occurs.
