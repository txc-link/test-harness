# Harness 工作流

Harness 将投资 Agent 想法转成有计划、可测试的工程工作。

## 一条命令

```powershell
cd D:\stock-agent\investment-agent-harness
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m harness_engine.cli run "你的需求"
```

## 分步执行

```powershell
iah init
iah intake "你的需求"
iah plan docs\requirements\REQ-0001.yaml
iah validate
pytest
```

## 产物流转

```text
docs/requirements/REQ-*.yaml
  -> docs/roadmap/REQ-*-roadmap.yaml
  -> docs/sprints/SPRINT-*.yaml
  -> docs/evals/EVAL-*.yaml
  -> tests/
```

## 完成定义

- 需求已经结构化。
- Roadmap 有里程碑和带门禁的任务。
- Sprint 有退出标准。
- 账户 alpha 和 skill evolution 有评估规格。
- `iah validate`、`ruff check .` 和 `pytest` 通过。
