## 1. Approval and immutable capture (not executed under HERM-173)

- [ ] 1.1 Obtain `APPROVE_PHASE2_TRANSACTION` from Herman.
- [ ] 1.2 Re-read all target objects; capture complete texts, hashes, revisions, protected fields, Squad leader/membership, Conveyor configuration, and HERM-118 constants.
- [ ] 1.3 Abort on conflicting intervening changes or failed HERM-118 hash/admission verification.

## 2. Acceptance harness prerequisite

- [x] 2.1 Implement versioned JSON schemas and a publication wrapper for artifacts, terminal envelopes, events, transitions, and metrics.
- [x] 2.2 Implement final-byte checks and adapter inventory; each adapter must prove pre-read predicate enforcement or fail before invocation.
- [x] 2.3 Implement all synthetic/schema fixtures and a completeness assertion over the scenario manifest.
- [ ] 2.4 Obtain independent Gate PASS on harness artifact/hash. Do not change live configuration before PASS.

## 3. Wake and dedup prerequisite

- [ ] 3.1 Prove the supported Multica event that enqueues the Orchestrator from terminal child completion/result evidence.
- [ ] 3.2 Prove duplicate EVENT_ID and TRANSITION_KEY create no additional task, issue, comment, or run.
- [ ] 3.3 Prove Conveyor remains comment-only and its wake is recovery-only after five minutes.

## 4. Compensated configuration transaction

- [ ] 4.1 Stage exact after texts for the five fields in `design.md`; compute hashes and protected-field comparisons.
- [ ] 4.2 Apply and read back all targets in one uninterrupted window.
- [ ] 4.3 On any mismatch, restore all written fields and verify exact before hashes.

## 5. Serial non-holdout replay

- [ ] 5.1 Execute the expected graph with synthetic/schema fixtures only and portfolio parallelism disabled.
- [ ] 5.2 Verify all acceptance scenarios, event/run identities, one-artifact/one-envelope publication, and independent Gates.
- [ ] 5.3 Publish machine-derived metrics with censoring and dedup keys; verify targets.
- [ ] 5.4 Roll back the transaction on any specified rollback trigger.

## 6. Review and later activation

- [ ] 6.1 Leave implementation issue in review with bilingual evidence, exact changed objects, before/after hashes, rollback status, and residual risks.
- [ ] 6.2 Keep portfolio parallelism disabled until a separately approved activation Gate meets `design.md` thresholds.
