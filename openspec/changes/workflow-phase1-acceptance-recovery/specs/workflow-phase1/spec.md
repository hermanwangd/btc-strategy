## ADDED Requirements

### Requirement: Executable producer acceptance

The workflow SHALL freeze a hashed synthetic-only acceptance bundle before Backtest dispatch and require producer and independent Gate execution.

#### Scenario: sealed read is attempted

- **WHEN** an adapter loads rows at or after 2024-01-01 before filtering
- **THEN** producer preflight fails before terminal publication and before any physical sealed-row read

### Requirement: Canonical evidence and bounded continuation

The workflow SHALL preflight canonical envelopes in-run, classify Gate defects, deduplicate successors, and permit only one qualifying post-Advanced bounded correction.

#### Scenario: repeated defect

- **WHEN** the same defect recurs after correction
- **THEN** automatic continuation stops with a named branch blocker and no successor
