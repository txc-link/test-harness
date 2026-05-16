# Harness Operating Model

This repository is the control plane for building the investment agent. It is not only a codebase. It is the place where product intent, engineering work, tests, release gates, investment evaluations, and controlled evolution are connected.

## End-To-End Flow

```text
idea
  -> intake
  -> discovery
  -> PRD
  -> RFC if architecture changes
  -> ADR if decision is accepted
  -> roadmap decomposition
  -> sprint planning
  -> implementation
  -> tests and evals
  -> CI
  -> release candidate
  -> staged release
  -> monitoring
  -> review
  -> evolution proposal
```

## Work Item Types

| Type | Location | Purpose |
| --- | --- | --- |
| Requirement | `docs/requirements/` | User problem and acceptance criteria |
| PRD | `docs/requirements/` | Product scope and behavior |
| RFC | `docs/rfc/` | Proposed technical or workflow change |
| ADR | `docs/adr/` | Accepted architecture or policy decision |
| Roadmap | `docs/roadmap/` | Milestones and decomposed tickets |
| Sprint | `docs/sprints/` | Near-term delivery plan |
| Test Plan | `docs/test-plans/` | Verification plan for risky work |
| Eval Spec | `docs/evals/` | Investment or agent-quality evaluation |
| Release | `docs/releases/` | Release checklist and notes |
| Review | `docs/reviews/` | Sprint, incident, or model review |
| Risk | `docs/risks/` | Risk register and mitigations |
| Runbook | `docs/runbooks/` | Repeatable operational procedures |

## Lifecycle States

Use these states for tickets, skills, evals, and releases:

```text
draft -> reviewed -> approved -> in_progress -> validating -> ready -> released -> monitored -> retired
```

For self-evolving skills:

```text
candidate -> backtested -> shadow_live -> approved -> active -> monitored -> retired
```

## Decision Rules

- If a change affects system architecture, create an RFC.
- If an RFC is accepted, record the decision as an ADR.
- If a change affects account risk, create or update an eval spec.
- If a change affects live trading, require human approval and rollback criteria.
- If a change affects skill evolution, require backtest and shadow-live gates.

