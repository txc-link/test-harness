# 开发环境

## Python

当前机器没有暴露普通 `python` 命令。请使用 Codex 随附的 Python：

```powershell
$PY = "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $PY -m pip install -e .[dev]
```

## 验证

```powershell
.\scripts\check.ps1
```

## Harness 命令

```powershell
& $PY -m harness_engine.cli init
& $PY -m harness_engine.cli intake "需求"
& $PY -m harness_engine.cli plan docs\requirements\REQ-0001.yaml
& $PY -m harness_engine.cli validate
& $PY -m harness_engine.cli run "需求"
& $PY -m harness_engine.cli new rfc "Harness Control Plane"
& $PY -m harness_engine.cli status --write
```

## Codex Skill

本地 Codex skill 已创建在：

```text
C:\Users\DELL\.codex\skills\investment-agent-harness
```

当需要 Codex 为本项目执行需求拆解、sprint 计划、评估门禁设计、CI/CD 设置或受控进化流程时，应使用该 skill。
