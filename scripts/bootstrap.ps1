$ErrorActionPreference = "Stop"

$Python = "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

& $Python -m pip install -e .[dev]
& $Python -m harness_engine.cli init
& $Python -m harness_engine.cli validate

