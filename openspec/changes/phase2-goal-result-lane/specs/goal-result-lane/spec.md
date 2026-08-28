## ADDED Requirements

### Requirement: Serial autonomous scorecard flow
The workflow MUST move every runnable, independently registered candidate through `REGISTERED -> BUILD -> PREHOLDOUT_BACKTEST -> PERFORMANCE_GATE -> RECONCILE` without human approval when all frozen contracts remain unchanged.

#### Scenario: Fast-path scorecard production
- **GIVEN** valid registration PASS, admitted HERM-118 evidence, available serial slot, frozen rules, and no holdout access
- **WHEN** every producer and independent Gate passes
- **THEN** exactly one reconciled pre-holdout CAGR/MDD scorecard exists within 24 hours and no downstream authority is granted

#### Scenario: Independent performance Gate
- **GIVEN** a valid pre-holdout backtest artifact
- **WHEN** the producer completes
- **THEN** only BTC Validation & Risk Gate may approve its scorecard, and producer evidence is not self-approval

#### Scenario: Unrelated branch continuation
- **GIVEN** one candidate has a branch-scoped blocker
- **WHEN** another registered candidate is runnable
- **THEN** the unrelated candidate continues subject to the existing 2+1 contract

### Requirement: Automatic and material decisions remain distinct
Routine frozen-scope work packages MUST auto-continue; only the decision categories enumerated in `design.md` MAY require Herman.

#### Scenario: Missing external authorization
- **GIVEN** a needed source requires a new credential, provider access, cost, or license
- **WHEN** no existing approval covers it
- **THEN** no source or functional dispatch occurs and one exact decision request is recorded

#### Scenario: Bounded implementation defect
- **GIVEN** prior findings PASS and one deterministic branch-local implementation defect changes no frozen contract
- **WHEN** it has an executable regression
- **THEN** exactly one bounded correction and one Gate are allowed without human approval
