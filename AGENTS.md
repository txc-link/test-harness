# Investment Agent Harness - Agent Guide

## Mission

Create and operate the engineering environment for a reviewable, testable, self-evolving investment agent. This repository is the harness layer: it governs requirements, decomposition, scheduling, testing, CI/CD, evaluation gates, and controlled evolution.

## Required Workflow

For every non-trivial request:

1. Classify the request: requirement, RFC, ADR, implementation, test, release, incident, or evolution proposal.
2. Capture new product intent as a structured requirement under `docs/requirements/`.
3. Create a PRD for user-facing behavior and an RFC for architecture or workflow changes.
4. Record accepted architecture or safety decisions as ADRs.
5. Decompose approved scope into milestones and gated tickets under `docs/roadmap/`.
6. Place near-term work into a sprint artifact under `docs/sprints/`.
7. Define tests, evaluation specs, or review gates before calling the work ready.
8. Run local validation before finalizing:

```powershell
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m harness_engine.cli validate
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m ruff check .
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest
```

## Project Stages

- `Discovery`: raw idea, reference project analysis, open questions.
- `Requirement`: structured problem, target user, scope, non-goals, acceptance criteria.
- `PRD/RFC/ADR`: product behavior, proposal, and accepted decision trail.
- `Plan`: roadmap, architecture decision, milestones, risks, gate matrix.
- `Sprint`: ticket selection, exit criteria, owners, expected tests.
- `Build`: implementation with tests and docs.
- `Evaluate`: lint, unit tests, integration tests, investment evals, shadow-live gates.
- `Release`: changelog, migration note, deployment checklist.
- `Evolve`: review failures, propose skill/config changes, gate promotion, monitor rollback.

## Mandatory References

Before substantial planning or implementation, consult:

- `docs/HARNESS_OPERATING_MODEL.md`
- `docs/QUALITY_GATES.md`
- `docs/DELIVERY_PIPELINE.md`
- `docs/RISK_CONTROL.md`

Use templates from `templates/` rather than inventing new formats.

## Investment-Specific Gates

- Any live-trading behavior must require human approval.
- Any skill promotion must pass backtest and shadow-live gates.
- Any account-risk change must include rollback criteria.
- Every recommendation feature must write to hypothesis and review ledgers.
- Every profitability claim must separate benchmark beta, strategy contribution, agent contribution, and user execution impact.

## Safety Boundaries

- Do not enable live trading by default.
- Do not auto-promote a strategy or skill without evidence.
- Do not treat LLM reflection as proof of improvement.
- Do not overwrite the four reference projects unless explicitly requested.
- Keep generated harness artifacts inside this repository unless the user asks otherwise.

## Reference Projects

The sibling projects are references, not edit targets by default:

- `../aiagents-stock`
- `../TradingAgents-astock`
- `../RD-Agent`
- `../deer-flow`
