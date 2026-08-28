## ADDED Requirements

### Requirement: Sole reusable prerequisite
The workflow MUST reuse HERM-118 and `SOURCE_ACQUISITION_CONTRACT_V2`; it MUST NOT create candidate-specific copies of the shared data-readiness dependency.

#### Scenario: Data reuse
- **GIVEN** identical frozen hashes and a valid existing HERM-118 admission
- **WHEN** a new candidate needs the shared inputs
- **THEN** the candidate reuses the admitted reference without copying source bytes or requesting human approval

#### Scenario: Hash drift decision
- **GIVEN** either registered hash differs
- **WHEN** verification runs
- **THEN** only dependent consumers pause and one deduplicated snapshot-version decision event is used; bytes are neither rejected nor silently adopted

#### Scenario: Existing equivalent source
- **GIVEN** an approved free, credential-free, provider-access-free, fee-free, license-free equivalent source
- **WHEN** the existing Source Gate passes it
- **THEN** resolution continues automatically; non-equivalent proxies remain research-only or quarantined

#### Scenario: Admission tier accuracy
- **GIVEN** HERM-118 is only `RESEARCH_ONLY`
- **WHEN** a pre-holdout scorecard is reconciled
- **THEN** it is labeled caveated research and cannot support final 2017–2026 qualification or holdout unseal
