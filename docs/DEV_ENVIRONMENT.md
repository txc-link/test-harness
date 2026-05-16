# Development Environment

## Python

This machine currently does not expose a normal `python` command. Use the bundled Codex Python:

```powershell
$PY = "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $PY -m pip install -e .[dev]
```

## Validate

```powershell
.\scripts\check.ps1
```

## Harness Commands

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

A local Codex skill was created at:

```text
C:\Users\DELL\.codex\skills\investment-agent-harness
```

Use it when asking Codex to run requirement decomposition, sprint planning, eval gate design, CI/CD setup, or controlled evolution workflow for this project.
