## ADDED Requirements

### Requirement: Supported result event wake
A valid terminal result MUST enqueue one Orchestrator task through a platform-supported trigger; a comment alone MUST NOT be assumed to trigger execution without run evidence.

#### Scenario: Result-event wake
- **GIVEN** one valid RESULT_READY_V2 event
- **WHEN** it becomes durable
- **THEN** one Orchestrator task is created within 60 seconds and its attribution references the event

#### Scenario: Duplicate wake
- **GIVEN** the same EVENT_ID is delivered twice or Conveyor repeats recovery
- **WHEN** the Orchestrator reconciles
- **THEN** no second task, successor issue, run, or transition is created

#### Scenario: Bounded recovery
- **GIVEN** valid evidence has no Orchestrator task for five minutes
- **WHEN** Project Conveyor patrols
- **THEN** it posts one deduplicated Orchestrator mention and performs no functional dispatch

#### Scenario: Runtime handoff failure
- **GIVEN** a trigger task fails before reconciliation
- **WHEN** the event remains unconsumed
- **THEN** one runtime retry is allowed without consuming implementation budget or duplicating functional work

#### Scenario: Repeated implementation defect
- **GIVEN** the same DEFECT_ID reappears after correction or a second new post-Advanced defect appears
- **WHEN** Gate publishes it
- **THEN** automatic retry stops with a named branch blocker
