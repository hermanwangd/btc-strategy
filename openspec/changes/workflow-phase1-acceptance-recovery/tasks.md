## 1. Configuration transaction

- [x] Snapshot five live objects and protected fields.
- [x] Stage and preflight complete after text.
- [x] Apply and verify all readback hashes.

## 2. Synthetic replay

- [x] Case A: producer preflight fast path and independent Gate — rejected fail-closed.
- [x] Case B: bounded new defect, deduplication, and repeat-defect stop — rejected fail-closed.
- [x] Reconcile one metrics record per case; 11/12 scenarios passed and rollback was verified.
