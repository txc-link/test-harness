# Agent Roles

The harness uses roles to separate concerns. One human or one coding agent may perform multiple roles, but the artifacts must remain distinct.

## Product Agent

- Converts raw ideas into PRDs and acceptance criteria.
- Protects user outcomes and non-goals.
- Owns `docs/requirements/`.

## Architect Agent

- Produces RFCs and ADRs.
- Defines module boundaries, integration contracts, and safety policies.
- Owns `docs/rfc/` and `docs/adr/`.

## Planner Agent

- Breaks requirements into milestones and sprint tickets.
- Ensures each ticket has gates and deliverables.
- Owns `docs/roadmap/` and `docs/sprints/`.

## Builder Agent

- Implements scoped changes.
- Adds tests and updates docs.
- Does not silently weaken gates.

## QA Agent

- Creates test plans.
- Verifies local and CI checks.
- Looks for regressions, missing evals, and untested risk.

## Release Agent

- Prepares release notes and rollback plans.
- Confirms staging, production, and monitoring readiness.

## Evolution Agent

- Reviews traces, failed cases, and performance metrics.
- Proposes candidate skill/config changes.
- Cannot promote high-risk changes without gates.

## Risk Agent

- Challenges assumptions.
- Classifies account, data, compliance, model, and operational risks.
- Can block release until mitigation exists.

