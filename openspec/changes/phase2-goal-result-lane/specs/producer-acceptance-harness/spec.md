## ADDED Requirements

### Requirement: Producer-local executable acceptance
Every producer MUST pass the frozen repository harness before terminal publication, and the independent Gate MUST rerun the exact hash-identified harness.

#### Scenario: Final-byte integrity
- **GIVEN** a stale hash, missing path, cache entry, invalid self-omission, or mismatched outer hash
- **WHEN** producer preflight runs from clean extraction
- **THEN** PASS and terminal publication are impossible

#### Scenario: Physical read-bound safety
- **GIVEN** an adapter would load a row at or after `2024-01-01T00:00:00Z` and filter later
- **WHEN** the preflight invokes it
- **THEN** it fails before reader invocation and records `READ_INVOCATIONS=0`

#### Scenario: Uninstrumented adapter
- **GIVEN** a storage adapter has no enforceable pre-read predicate proof
- **WHEN** it is selected
- **THEN** the harness fails closed before any data read

#### Scenario: One artifact and envelope
- **GIVEN** multiple artifacts, multiple terminal envelopes, missing typed fields, or a hash mismatch
- **WHEN** publication wrapper validation runs
- **THEN** nothing terminal is published and the defect is repaired in-run without a correction issue

#### Scenario: Independent Gate retains authority
- **GIVEN** producer preflight PASS
- **WHEN** Gate reruns the harness
- **THEN** Gate may independently reject and producer PASS never counts as approval
