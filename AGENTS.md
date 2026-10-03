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

## Final response expectations

Every implementation or proposal should clearly answer:

- Which requirement in [requirement.md](requirement.md) this work addresses
- What changed
- Why the change is needed
- How it was validated

## Priority

The requirement baseline has higher priority than ad hoc implementation suggestions.
If the requirement and the proposed implementation conflict, the requirement wins.
