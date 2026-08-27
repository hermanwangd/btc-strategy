## 1. Implementation review (not executed under HERM-131)

- [ ] 1.1 Obtain separate approval to change `BTC Workflow Orchestrator.instructions` and the `BTC_Strategy_Multica` project description.
- [ ] 1.2 Re-read and archive exact pre-change values for rollback; confirm no intervening contract change conflicts with this specification.
- [ ] 1.3 Apply only the exact replacement clauses in `design.md`; do not change any other Multica object.

## 2. Runtime contract wiring (not executed under HERM-131)

- [ ] 2.1 Register V1 metadata on HERM-118 without copying or transforming source bytes.
- [ ] 2.2 Add hash-first validation, deterministic event deduplication, decision-envelope validation, branch-scoped pause, and access/handoff classifications.
- [ ] 2.3 Add independent admission-tier recording to Source Gate handoff while preserving `RESULT_DISPOSITION`.
- [ ] 2.4 Add dependency-lineage invalidation and immutable version registration.

## 3. Acceptance verification (not executed under HERM-131)

- [ ] 3.1 Verify matching hashes continue without human approval.
- [ ] 3.2 Verify drift blocks unapproved bytes, pauses only dependents, and emits exactly one event.
- [ ] 3.3 Verify repeated drift deduplicates and a distinct tuple permits a distinct event.
- [ ] 3.4 Verify both `KEEP_CURRENT_SNAPSHOT` availability paths and `ADOPT_NEW_SNAPSHOT` selective invalidation.
- [ ] 3.5 Verify local-unavailable and `HTTP 403` classifications route internal repair.
- [ ] 3.6 Verify `RESEARCH_ONLY` claim prohibition and `CANONICAL_ELIGIBLE` strict evidence requirement.
- [ ] 3.7 Verify no source mutation/copy, duplicate HERM-118, HERM-129/HERM-130 rewrite, unrelated pause, holdout unseal, promotion, deployment, capital, paper/live, or trading action.
- [ ] 3.8 Verify an identical tuple after `KEEP_CURRENT_SNAPSHOT` reuses durable evidence and waits in `WAITING_FOR_V1_RESTORE` without a duplicate event when V1 is unavailable.
- [ ] 3.9 Verify a stale `ADOPT_NEW_SNAPSHOT` decision cannot authorize a newly changed tuple.
- [ ] 3.10 Verify an agent or non-Herman member cannot authorize a transition by spoofing `DECISION_AUTHORITY=Herman Wang`.

## 4. Rollback rehearsal (not executed under HERM-131)

- [ ] 4.1 Restore exact prior text in a non-production rehearsal and verify all V2 evidence remains retained.
- [ ] 4.2 Record implementation evidence and request independent review before runtime activation.
