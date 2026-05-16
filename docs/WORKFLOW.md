# Harness Workflow

The harness turns an investment-agent idea into planned, testable engineering work.

## One Command

```powershell
cd D:\stock-agent\investment-agent-harness
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m harness_engine.cli run "你的需求"
```

## Step By Step

```powershell
iah init
iah intake "你的需求"
iah plan docs\requirements\REQ-0001.yaml
iah validate
pytest
```

## Artifact Flow

```text
docs/requirements/REQ-*.yaml
  -> docs/roadmap/REQ-*-roadmap.yaml
  -> docs/sprints/SPRINT-*.yaml
  -> docs/evals/EVAL-*.yaml
  -> tests/
```

## Definition Of Done

- Requirement is structured.
- Roadmap has milestones and gated tickets.
- Sprint has exit criteria.
- Evaluation specs exist for account alpha and skill evolution.
- `iah validate`, `ruff check .`, and `pytest` pass.

