## Evidence and current-state map

Evidence cutoff is `2026-08-28T04:54:16Z` (HERM-173 creation). The primary cohort is HERM-114 plus 43 descendants; HERM-160 is excluded from candidate-output counts. Later activity changes censoring time, not the observed funnel: `6 hypotheses -> 3 registration PASS -> 2 builds -> 1 build Gate PASS -> 0 performance Gates -> 0 qualified candidates`. HERM-171 is a parked, independently registered TRENDQUALITY ledger and is the clean replay candidate identity; parking is not authorization to execute it.

```text
registration -> registration Gate -> shared HERM-118 readiness
                                      |
                                      v
candidate ledger -> Basic build -> Gate -> Advanced correction -> Gate -> terminal
                                                             (HERM-139..145)

expected Phase-2:
HERM-118 admitted + REGISTERED
  -> BUILD -> BUILD_GATE(PASS)
  -> PREHOLDOUT_BACKTEST -> PERFORMANCE_GATE
  -> RECONCILE(scorecard or evidence-backed terminal state)
```

Observed controls: HERM-118 is `done`, hashes and `CUTOFF_2026=2026-05-22` are pinned, admission is `RESEARCH_ONLY`, source bytes were not copied, and the sealed `2024-01-01..2026-05-22` holdout remains closed. `RESEARCH_ONLY` permits caveated pre-holdout research, never final 2017–2026 qualification claims.

The quantified baseline remains the issue-author baseline because no later HERM-114 descendant produced a performance Gate: effective scorecard throughput `0/day`; registration first-disposition P50 about `19m40s`; usable registration PASS P50 about `1h25m` (n=3); agent time 56.8% research/enabling, 2.4% necessary first Gate, 30.5% coordination, 10.3% correction/retry; no-active-run proxy `26h43m/39h48m=67.1%`; rework `13/42=31.0%`. These denominators exclude HERM-160 synthetic children and treat open HERM-171 as right-censored, not failed.

## Root-cause delta from rolled-back Phase 1

| Failure | Phase-1 assumption | Verified evidence | Phase-2 correction |
|---|---|---|---|
| Physical boundary | A synthetic checker could prove safe reads | HERM-164 found the “positive” path read a `2024-01-02` sentinel before filtering | Instrument the real adapter boundary; fail before reader invocation; Gate runs the same binary/tests |
| Envelope | Prompt preflight could enforce typed publication | HERM-160 reports typed Gate-envelope enforcement was not executable | JSON Schema/validator plus publication wrapper; one artifact and one terminal envelope |
| Fixture completeness | Clauses implied complete scenarios | HERM-168 rejected because `DEPENDENCY` fixture was absent | Fixture inventory is versioned and completeness-tested before replay |
| Wake | Parent `RESULT_READY_V1` implied a task | Three HERM-162 events needed explicit recovery mentions | Supported trigger proof is an acceptance prerequisite; event and transition ledgers are separate |
| Outcome flow | Build completion was the practical terminus | HERM-114 has zero performance Gates | Add explicit pre-holdout backtest and performance Gate states |

## Approaches and impact order

1. **Recommended: repository harness + serial runtime clauses + supported wake.** Highest throughput and safety confidence; medium effort; reversible through one compensated transaction. It directly reaches a scorecard and removes late administrative defects.
2. **Prompt-only serial lane.** Low effort, but HERM-160 already disproved enforceability and fixture completeness. Reject.
3. **New workflow service/engine.** Strong enforcement but high effort and outside current authorization; unnecessary unless Multica cannot expose a supported terminal-result trigger. Defer and return `REVISE_PHASE2_DESIGN` if that platform prerequisite fails.

Impact order is: autonomous scorecard lane, HERM-118 reuse, shifted-left acceptance, event continuation, then portfolio parallelism. Dependency-safe implementation order is: verify HERM-118 -> build harness -> prove wake/dedup -> stage clauses -> serial replay -> later parallelism Gate.

## Automatic-continue and human-decision envelopes

Automatic continuation is legal only when candidate registration, rules, identities, inputs, costs, financing, accounting, execution lag, cutoff, data version/tier, pre-2024 evaluation bounds, permissions, and `--no-holdout` remain frozen; HERM-118 admission is valid; the next work package is routine BUILD, PREHOLDOUT_BACKTEST, PERFORMANCE_GATE, or RECONCILE; a registered `2+1` slot is available; and no identical non-terminal transition exists. Routine child creation is not a material decision.

Herman is required only for a new snapshot-version decision, credentials/provider access/cost/license, unavailable approved reference after bounded internal repair, material strategy/rule/input/cost/accounting/cutoff/data/engine/holdout/permission change, retry-budget extension, finalist nomination/unseal, promotion, deployment, paper/live, capital, orders, or trading. Technical defects, access/handoff repair, already approved equivalent sources, and branch-local bounded fixes do not become human decisions.

## Exact proposed Multica objects and clauses

All text below is additive to the named field unless an implementation diff proves an exact narrower replacement. Immediately before staging, archive complete live text, SHA-256, revision, and protected fields.

### BTC Workflow Orchestrator (`8cb3efc1-c123-4bf2-ab4a-af173e0570bc`). Field: `instructions`

Before: live contract ends routine candidate progression at producer/Gate reconciliation and Advanced terminal stop; it says immediate handoff but defines no proven terminal-result trigger and no performance-scorecard state machine.

After clause:

```markdown
## Phase-2 autonomous goal-result lane
For an independently registered runnable candidate with a satisfied HERM-118 admission, execute exactly:
`REGISTERED -> BUILD -> PREHOLDOUT_BACKTEST -> PERFORMANCE_GATE -> RECONCILE`.
Each transition MUST validate predecessor run, typed terminal envelope, artifact hashes, HERM-118 admission, frozen candidate contract, `--no-holdout`, and the registered 2+1 slot. Deduplicate by `TRANSITION_KEY=sha256(candidate_id|stage|predecessor_result_identity|artifact_sha256|correction_ordinal)`. At most one non-terminal successor may exist. Routine in-envelope work-package creation MUST continue without human approval. A PERFORMANCE_GATE PASS creates one reconciled pre-holdout scorecard record; it is not final qualification or holdout authority.

Terminal publication MUST use the versioned repository `PHASE2_ACCEPTANCE_HARNESS` and typed publication wrapper. A producer cannot PASS unless final-byte, physical-reader-bound, schema, identity/hash, exactly-one-artifact, and exactly-one-envelope checks pass. Gate reruns the same frozen harness independently.

`RESULT_READY_V2` MUST carry EVENT_ID, TASK_ID, RUN_ID, parent/child/candidate/stage, disposition, artifact IDs/hashes, harness ID/hash, and NEXT_STATE. Supported terminal-result trigger evidence MUST enqueue this Orchestrator. Deduplicate wakes by EVENT_ID and transitions by TRANSITION_KEY. Project Conveyor may only post one deduplicated recovery mention after five minutes with no task; it may not create, assign, or dispatch functional work.

Classify failures as EVIDENCE_ENVELOPE, RUNTIME_HANDOFF, RECOVERABLE_DEPENDENCY, REPEAT_IMPLEMENTATION, NEW_BOUNDED_IMPLEMENTATION, or MATERIAL_CONTRACT. Repair envelope defects in-run; retry runtime handoff once without functional duplication; bind shared dependency to HERM-118; permit exactly one branch-local bounded correction with regression evidence; stop on repeat defect or a second post-Advanced new defect; request Herman only for MATERIAL_CONTRACT or listed approval categories.
```

Protected: name, description, model, runtime, thinking/service tier, skills, MCP/env, permissions, visibility, concurrency, membership, leader.

### Basic and Advanced Backtest Engineers

Objects: Basic `07b722f9-510f-42ea-a2df-39f0857efd09`; Advanced `b0db089c-a391-4210-b83a-54b5a3e35582`. Field: `instructions`.

Before: restored pre-transaction instructions; no enforceable versioned harness or typed wrapper.

After clause (same invariant, lane-specific retry authority remains distinct):

```markdown
## Phase-2 producer preflight
Before terminal publication, execute the frozen `PHASE2_ACCEPTANCE_HARNESS` from a clean extraction using only schema/synthetic fixtures. `PACKAGE_FINAL_BYTES_V2` MUST verify manifest paths, canonical hashes, cache exclusion, self-omission, and outer artifact hash. `SEALED_IO_BOUNDARY_V2` MUST wrap each real storage adapter and assert an enforceable physical predicate `<2024-01-01T00:00:00Z` before invocation; missing/malformed bounds, load-before-filter, or an uninstrumented adapter MUST fail with READ_INVOCATIONS=0. `RESULT_ENVELOPE_V2` MUST validate typed fields, actual attachment hashes, one artifact, one envelope, and canonical identities. Publish nothing terminal until all checks pass. Producer PASS is not independent approval.
```

Protected: all fields above plus frozen candidate strategy, data, engine-interface, cutoff, cost, accounting, and holdout contracts. Advanced remains escalation-only.

### BTC Validation & Risk Gate (`21799e12-394e-4b66-a0f5-e7267d0decb9`). Field: `instructions`

Before: independent review exists but restored text has no enforceable Phase-2 harness requirement.

After clause:

```markdown
## Phase-2 independent performance review
Independently rehash producer bytes and rerun the exact frozen harness from clean extraction. Verify source and validation artifact identities separately. For PREHOLDOUT_BACKTEST, verify causal lag, pre-2024 physical reads, declared costs/financing/accounting, reproducibility, CAGR and MDD calculation, and no candidate-conditioned sealed-holdout access. Return one typed PASS|REJECTED|BLOCKED envelope with normalized defect fields. PASS validates one pre-holdout scorecard only and grants no holdout unseal, final qualification, promotion, deployment, capital, paper/live, order, or trading authority.
```

Protected: all non-instructions fields and independent ownership; producer may not self-approve.

### BTC_Strategy_Multica (`b67b7971-cfeb-4067-992a-4119fe7f9cf9`). Field: `description`

Before: authoritative goal, Conveyor, Orchestrator, HERM-118/V2 source, 2+1, holdout, and approval contracts; no explicit full pre-holdout scorecard chain.

After clause:

```markdown
## Phase-2 serial scorecard contract
After HERM-118 admission and independent registration PASS, runnable candidates continue through `REGISTERED -> BUILD -> PREHOLDOUT_BACKTEST -> PERFORMANCE_GATE -> RECONCILE`. Routine frozen-scope work packages are automatic. Target: >=1 valid independently reviewed pre-holdout CAGR/MDD scorecard per rolling 24h and >=80% registration-PASS-to-performance-Gate conversion for runnable candidates. HERM-118 remains sole shared prerequisite; SOURCE_ACQUISITION_CONTRACT_V2, admission tiers, hash-drift decision, sealed holdout, independent Gate, 2+1 meaning, Conveyor comment-only boundary, and approval categories remain unchanged. Portfolio parallel dispatch remains disabled until the separate activation Gate passes.
```

Protected: project name/status/resources, source constants/bytes, cutoff, holdout/unseal, thresholds, 2+1 semantics, and all downstream authority boundaries.

### Project Conveyor autopilot

Before/after: **no configuration change**. Existing object identity, prompt, `run_only` mode, 15-minute schedule, permissions, labels, and assignee remain protected. Replay verifies it can post only one recovery mention after the five-minute SLO and cannot dispatch.

### Squad `BTC Investment Strategy Squad` (`5fcd5a4a-1272-4ca2-be41-ee97268eca35`)

Before/after: **no configuration change**. Leader must remain BTC Workflow Orchestrator; membership, routing, and concurrency semantics remain unchanged.

## Replay graph and event identities

Use a dedicated `WORKFLOW_PHASE2_NON_HOLDOUT_REPLAY` parent and HERM-171 identity copied as schema fields only; never read candidate or holdout data. Expected fast-path graph: harness-build -> independent harness Gate -> synthetic BUILD producer -> build Gate -> synthetic PREHOLDOUT_BACKTEST producer -> PERFORMANCE_GATE -> reconciliation. Each producer/Gate has one run, one artifact, one terminal envelope, and one parent `RESULT_READY_V2`. Event key is `sha256(task_id|run_id|result_identity|artifact_sha256)`; transition key is defined above. Duplicate event replay creates no issue or run.

The replay includes every scenario in the capability specs, publishes one metrics record per case, and fails the complete transaction on a safety defect, duplicate dispatch, missing supported wake, incomplete fixture, or typed-validator bypass.

## Metrics dictionary

| Metric | Definition |
|---|---|
| Valid scorecards/day | Numerator: unique PERFORMANCE_GATE PASS scorecards with verified artifact hash and pre-holdout boundary. Denominator: rolling 24h; dedup by candidate+rules hash+data version+run. Registration/build artifacts are excluded. |
| Conversion | Runnable registration PASS candidates reaching any valid PERFORMANCE_GATE disposition / runnable registration PASS candidates admitted in cohort. Exclude named external waits; right-censor active candidates. |
| Registration Gate P50 | Median from producer registration terminal event to first usable independent registration PASS. Rejections remain observations for first-disposition metric only. |
| First-pass acceptance | Producers whose first terminal publication passes producer preflight and first independent Gate administrative checks / all producer first attempts. Strategy-performance rejection is not an administrative failure. |
| Rework rate | Correction/retry/re-Gate issues / completed functional+Gate descendants; exclude recovery-only wake comments and synthetic replay from live cohort. |
| Wake latency | Orchestrator task `created_at` minus valid RESULT_READY event `created_at`; one observation per EVENT_ID. |
| Successor latency | successor run `created_at` minus reconciliation comment `created_at`; dedup by TRANSITION_KEY. |
| Runnable idle | union wall-clock seconds where runnable branch has no non-terminal task/review/transition; overlapping intervals count once. |
| Blocked/wait share | named WAITING interval union / replay wall-clock from intake to reconciliation. |
| Agent time | sum of run `completed_at-started_at`; may exceed wall-clock under overlap. Wall-clock is final reconciliation minus intake. |
| Snapshot reuse | candidates using already Gate-admitted identical HERM-118 snapshot / candidates requiring that dependency. |
| Safety | unique holdout access, source mutation/copy, duplicate successor, or unauthorized transition incidents; target zero. |

## Rollback and residual risk

Use `TRANSACTION_MODE=COMPENSATED_ALL_OR_ROLLBACK`. Capture complete before texts/hashes and protected fields; stage all after texts/hashes; apply in one window; read back; then replay. Roll back all changed fields on any readback mismatch, safety regression, duplicate dispatch, unsupported result trigger, fail-open adapter, validator bypass, fixture incompleteness, or contradictory clause. Restore exact bytes including trailing newline, verify all pre-hashes, and retain repository/issue/replay evidence.

Residual risks: Multica may not expose a supported arbitrary result-comment trigger; adapters may exist outside the harness inventory; prompt execution can still omit a command; `RESEARCH_ONLY` can be misread as qualification. Mitigations are trigger proof before transaction, adapter inventory fail-closed, wrapper-generated publication, Gate rerun, and explicit claim labels. If supported wake proof fails, do not install clauses; return `REVISE_PHASE2_DESIGN` rather than build a new engine.

## Portfolio activation Gate (not enabled)

Only after the serial replay meets all safety targets and, in two consecutive non-holdout observations, produces >=1 valid scorecard/24h, >=80% conversion, <10% rework, >=90% first-pass acceptance, wake P95 <60s, successor P95 <2m, runnable idle >5m = 0, and wait share <20%, Herman may separately approve 2–3 independent hypothesis families. Each must have distinct hypothesis/family IDs, multiple-testing ledger, cheap causal falsifier before full backtest, frozen no-holdout contract, and independent Gate. Post-activation targets are >=2 scorecards/day, >=80% distinct-family ratio, and zero holdout incidents.
