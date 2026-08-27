## Specification-level acceptance review

Review date: 2026-08-27. Scope: static review of the formal specification; no runtime implementation was executed.

| # | Scenario | Result | Normative evidence |
|---|---|---|---|
| 1 | Frozen hashes match | PASS | `immutable direct-reference registration` and `frozen hashes match` require hash-first validation and continuation without approval. |
| 2 | Either hash differs | PASS | `snapshot-version drift detection and isolation` prohibits calculation use, limits the pause, and activates one event. |
| 3 | Same drift repeats | PASS | `deterministic approval event` defines exact tuple hashing and unresolved-event reuse. |
| 4 | Different tuple appears | PASS | `distinct drift tuple` permits one identity-distinct event. |
| 5 | `KEEP_CURRENT_SNAPSHOT` | PASS | Both readable and unavailable V1 scenarios preserve authority, reject observed bytes, and scope waiting. |
| 6 | `ADOPT_NEW_SNAPSHOT` | PASS | Requires immutable V2, permanent V1 evidence, Source Gate rerun, and lineage-limited invalidation/rebuild. |
| 7 | Local unavailable / `HTTP 403` | PASS | `access and handoff error classification` routes internal repair and prohibits `REJECTED`/reacquisition. |
| 8 | `RESEARCH_ONLY` | PASS | Allows caveated research and forbids final qualification and CAGR/MDD claims. |
| 9 | `CANONICAL_ELIGIBLE` | PASS | Requires strict point-in-time/revision evidence before final qualification eligibility. |
| 10 | Forbidden side effects | PASS | `invariant boundaries` prohibits source copy/mutation, duplicate HERM-118, HERM-129/HERM-130 rewrite, unrelated pause, and downstream authorization. |
| 11 | Identical tuple after `KEEP_CURRENT_SNAPSHOT` | PASS | Durable event identity survives resolution; the same tuple reuses its event/decision and uses `WAITING_FOR_V1_RESTORE` without another event when V1 is unavailable. |
| 12 | Stale `ADOPT_NEW_SNAPSHOT` decision | PASS | Immediate hash recomputation prevents the old decision from authorizing a changed tuple and requires one event for the current identity. |
| 13 | Spoofed `DECISION_AUTHORITY` | PASS | The authority string is insufficient; the comment author must resolve to Herman Wang's authorized workspace member and user IDs or the result is `DECISION_RECORD_ERROR`. |

## Contradiction review

- **Independent Source Gate:** preserved; adoption approves a version but MUST rerun Source Gate and does not approve quality.
- **Comment-only watchdog:** preserved; Project Conveyor receives no mutation or dispatch authority.
- **HERM-118 dependency lane:** preserved and reused as the sole event/decision ledger; no duplicate parent is permitted.
- **Project objective:** preserved; `RESEARCH_ONLY` cannot support the net `CAGR > 80%` / absolute `MDD < 50%` qualification claim, while `CANONICAL_ELIGIBLE` only admits work to the remaining frozen gates.
- **Sealed holdout and downstream authority:** unchanged; the specification authorizes no unseal, qualification shortcut, promotion, deployment, capital, paper/live, or trading action.

No unresolved contradiction was found at specification level. Implementation remains separately gated and must re-read live text for intervening changes before applying the exact replacements.
