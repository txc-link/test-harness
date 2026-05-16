# Investment Agent Harness

This is the engineering harness for building a reviewable, testable, self-evolving investment agent.

It is intentionally separate from the four reference projects under `D:\stock-agent`. The harness owns the mature delivery workflow:

```text
idea
  -> intake
  -> discovery
  -> PRD/RFC/ADR
  -> roadmap
  -> sprint plan
  -> implementation ticket
  -> tests/evals
  -> CI/CD
  -> release
  -> monitoring
  -> review
  -> controlled evolution proposal
```

## Quick Start

```powershell
cd D:\stock-agent\investment-agent-harness
python -m pip install -e .[dev]
iah init
iah intake "建立可复盘、可自我进化的投资 Agent，先支持 A股和美股的持仓、盯盘、假设账本、复盘和 Skill 进化门禁。"
iah plan docs\requirements\REQ-0001.yaml
iah validate
pytest
```

## What This Harness Produces

- Structured requirement records in `docs/requirements/`
- Decomposed milestones in `docs/roadmap/`
- Sprint-ready tickets in `docs/sprints/`
- Evolution and profitability evaluation specs in `docs/evals/`
- Architecture decisions in `docs/adr/`
- RFCs in `docs/rfc/`
- Test plans in `docs/test-plans/`
- Release checklists in `docs/releases/`
- Runbooks in `docs/runbooks/`
- Reviews, risks, incidents, and metrics records

## Core Operating Docs

- [Harness Operating Model](docs/HARNESS_OPERATING_MODEL.md)
- [Harness Engine](docs/HARNESS_ENGINE.md)
- [Harness Maturity Model](docs/HARNESS_MATURITY_MODEL.md)
- [Agent Roles](docs/AGENT_ROLES.md)
- [Quality Gates](docs/QUALITY_GATES.md)
- [Delivery Pipeline](docs/DELIVERY_PIPELINE.md)
- [Risk Control](docs/RISK_CONTROL.md)
- [Observability And Metrics](docs/OBSERVABILITY_METRICS.md)
- [CI/CD Plan](docs/CICD.md)
- [Development Environment](docs/DEV_ENVIRONMENT.md)
- [Harness Skill Stack](docs/SKILL_STACK.md)

## Operating Principles

1. Every investment recommendation must become a tracked hypothesis.
2. Every hypothesis must have an expiry, invalidation condition, benchmark, and review path.
3. Agent improvement is not trusted until it passes evaluation gates.
4. Live-account changes require human approval by default.
5. Skills are versioned, evaluated, promoted, and rollback-capable.

## Local Validation

```powershell
.\scripts\check.ps1
```

This runs harness validation, lint, and tests.
