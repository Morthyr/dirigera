# Repository Instructions

This repository uses the project requirement baseline as the source of truth for all change requests and implementation work.

## Mandatory workflow

Before proposing or implementing any code change, the agent must:

1. Read and understand [requirement.md](requirement.md).
2. Identify the relevant requirement section for the requested work.
3. Confirm the scope, constraints, and acceptance criteria before making changes.
4. Implement only work that is traceable to the requirement baseline.
5. Summarize the result by referencing the requirement section(s) it satisfies.

## Rule of operation

- Do not implement features or fixes that are not aligned with the requirement baseline.
- Do not make assumptions that conflict with the documented current system context.
- If a requirement is missing, unclear, or outdated, stop and ask for clarification before changing code.
- If a new requirement is needed, update [requirement.md](requirement.md) first and then proceed.

## Project baseline

The current project context is stored in [requirement.md](requirement.md). It describes:

- the current system behavior,
- the repository purpose,
- the current functionality,
- operational assumptions,
- the reusable CR template for future work.

## Testing workflow

The repository includes a Windows test runner at [test.bat](test.bat). The expected workflow is:

1. Run [test.bat](test.bat) from the repository root.
2. The script installs the project dependencies from [requirements.txt](requirements.txt).
3. The script runs the test suite with pytest.
4. The change is only complete when the test command exits successfully.

## Runtime workflow

The repository must provide a working application launcher at [start.bat](start.bat).

- [start.bat](start.bat) is the supported way to run the project from the repository root.
- It must install required dependencies if needed and start the Python application entry point.
- The agent must ensure the startup command remains runnable and does not depend on an arbitrary working directory.

## Change request expectations

For any CR or feature request, the agent should produce or update a requirement entry using the structure in [requirement.md](requirement.md), including:

- Summary
- Background and context
- Scope
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Validation and testing
- Risks and rollback

## Mandatory testing rule

Every function must be covered with unit tests, and every user-facing use case must be covered with end-to-end tests before the change is considered complete.

- Unit tests are required for all implemented functions, including helper functions and state-transition logic.
- End-to-end tests are required for each meaningful workflow the user can execute in the application.
- Test coverage must be run and verified locally before completion.
- If the repository has no tests yet, the agent must create the required test suite as part of the work.

## Final response expectations

Every implementation or proposal should clearly answer:

- Which requirement in [requirement.md](requirement.md) this work addresses
- What changed
- Why the change is needed
- How it was validated

## Priority

The requirement baseline has higher priority than ad hoc implementation suggestions.
If the requirement and the proposed implementation conflict, the requirement wins.
