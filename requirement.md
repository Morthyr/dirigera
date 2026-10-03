# AI Agent Requirement Context Template

This file acts as the project baseline for future change requests (CRs) and AI-assisted work in this repository. It combines:

1. a summary of the current system behavior, and
2. a reusable template for documenting future requirements.

The purpose is to give any future AI agent enough context to understand what the project does today before proposing or implementing a change.

---

## 1. Current System Context

### Repository purpose
This repository is a lightweight Python client for an IKEA DIRIGERA smart home hub. It establishes a secure websocket connection to the DIRIGERA device, listens for device events, and prints event payloads to the console.

### Current functionality
The current implementation has the following behavior:

- Reads a cached authentication token from `dirigera_token.txt`.
- If no token exists, prompts the user to press the DIRIGERA action button and runs the system `generate-token` command for the configured hub IP.
- Extracts the bearer token from the CLI output and stores it locally for reuse.
- Connects to the DIRIGERA websocket endpoint at `wss://<IP>:8443/v1` using an Authorization bearer token.
- Sends an initial empty JSON payload to initialize the connection and then subscribes to events by sending:

  {
    "action": "subscribe",
    "id": "events"
  }

- Receives and logs incoming JSON events in a readable, indented format.
- Detects event payloads containing the configured `BADØYE_ID` and prints a special alert line indicating a Badøye-related event.
- Handles websocket errors and connection closes.
- Automatically reconnects in a loop after a normal disconnect.
- If the token is rejected with a 401/403 response, deletes the cached token, requests a new one, and reconnects with the fresh token.
- Uses `ssl.CERT_NONE` during websocket connection setup, meaning the script intentionally does not validate the hub certificate.

### Current file structure and role
- `dirigera.py`: main entry point; token handling, websocket logic, reconnect loop, and event monitoring.
- `dirigera_token.txt`: cached bearer token used to avoid re-authentication on next startup.
- `devices.json`: likely stores device metadata or device state snapshots (needs documentation when used by a future CR).
- `start.bat`: convenience script for starting the Python process on Windows.
- `test.bat`: Windows test runner that installs the required Python dependencies and executes the repository test suite.
- `requirements.txt`: Python dependency list for runtime and test setup.
- `tests/test_dirigera.py`: repository test suite covering current functionality.

### Operational assumptions
- The project assumes a local DIRIGERA gateway reachable at `192.168.0.6`.
- It is designed for console-based monitoring rather than a web UI or API server.
- It currently logs events but does not persist them into a database or expose them as a service.
- It is focused on event observation and token lifecycle management rather than device control.
- The project must provide a working startup entry point via `start.bat` so the application can be launched from the repository root.

---

## 2. Requirement Template for Future CRs

Use the following structure for each new change request. The goal is to describe the change clearly enough that a future AI agent can understand the background, scope, technical constraints, and expected outcome without needing to reverse-engineer the project.

### CR Metadata

- CR ID:
- Title:
- Author:
- Date:
- Status: Draft / Approved / In Progress / Done
- Related issue / ticket:
- Priority: High / Medium / Low

### 2.1 Summary

- Problem statement:
- Desired outcome:
- Why this change is needed:
- Expected business or operational benefit:

### 2.2 Background and Context

Describe the current behavior relevant to the requested change.

- Current system behavior:
- Existing assumptions:
- Related components or files:
- Known limitations or constraints:
- External dependencies:

### 2.3 Scope

#### In Scope
- 
- 
- 

#### Out of Scope
- 
- 
- 

### 2.4 Functional Requirements

Write each requirement as a testable statement.

1. The system shall...
2. The system shall...
3. The system shall...

### 2.5 Non-Functional Requirements

- Performance:
- Reliability:
- Security:
- Compatibility:
- Maintainability:
- Logging / observability:
- User experience:
- Testing mandate: Every function in the codebase must have unit-test coverage, and every user-facing workflow or use case must have end-to-end test coverage.

### 2.6 Data and Integration Requirements

- Input data contract:
- Output data contract:
- External API or system interaction:
- Error handling expectations:
- Persistence requirements:
- Backward compatibility requirements:

### 2.7 User Story / Scenario

- As a ...
- I want ...
- So that ...

### 2.8 Acceptance Criteria

Acceptance criteria should be objective and verifiable.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] Criterion 4

### 2.9 Validation and Testing

- Unit tests:
- Integration tests:
- Manual validation steps:
- Edge cases:
- Regression checks:

### 2.10 Risks and Rollback

- Main risks:
- Mitigation plan:
- Rollback or fallback strategy:

### 2.11 Implementation Notes

- Files likely to change:
- Existing code patterns to follow:
- Known constraints:
- Alternative options considered:

### 2.12 Sign-off

- Product / owner:
- Engineering:
- QA:
- Date:

---

## 3. Guidance for Future AI Agents

When creating or updating a CR, the agent should:

1. Start from the current system context in this file.
2. Describe the current behavior before proposing any change.
3. State the problem, desired outcome, and scope precisely.
4. Prefer testable requirements over vague suggestions.
5. Always list acceptance criteria and validation steps.
6. Note external dependencies and operational constraints.

This keeps the project documentation aligned with what the software actually does today and makes future CRs easier to evaluate consistently.
