$ErrorActionPreference = "Stop"

$Python = "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

& $Python -m harness_engine.cli validate
& $Python -m harness_engine.cli status --write
& $Python -m ruff check .
& $Python -m pytest
