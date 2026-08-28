## ADDED Requirements

### Requirement: Machine-observable metrics
Metrics MUST be derived from issue, run, event, artifact, or repository-test timestamps and identities using the dictionary in `design.md`.

#### Scenario: Metrics accuracy
- **GIVEN** a replay graph with duplicate events and overlapping runs
- **WHEN** metrics are calculated
- **THEN** events are deduplicated, agent time is separate from union wall-clock time, active observations are right-censored, and registration/build artifacts are not scorecards

#### Scenario: Rollback
- **GIVEN** any safety, trigger, deduplication, validator, fixture, or readback failure
- **WHEN** the transaction is evaluated
- **THEN** every changed field is restored to its exact prior hash while evidence remains immutable

#### Scenario: Parallelism remains off
- **GIVEN** the serial replay has not met every activation threshold twice
- **WHEN** multiple hypothesis families are ready
- **THEN** no new portfolio-parallel dispatch is enabled
