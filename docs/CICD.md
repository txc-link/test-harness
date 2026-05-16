# CI/CD Plan

## Current CI

GitHub Actions workflow:

- `.github/workflows/ci.yml`

Runs:

```text
python -m pip install -e .[dev]
python -m harness_engine.cli validate
ruff check .
pytest
```

## Local Equivalent

Use:

```powershell
.\scripts\check.ps1
```

## CD Strategy

Phase 1 has no production deployment. CD means publishing validated planning artifacts.

Phase 2 should add:

- artifact packaging
- docs site build
- versioned schema release

Phase 3 should add:

- staging deploy
- migration checks
- shadow-live worker deploy
- manual promotion approval

## Required Release Gates

- CI green
- `docs/requirements/` updated for new scope
- `docs/roadmap/` updated for milestone changes
- `docs/evals/` updated for investment evaluation changes
- ADR added for architecture or safety policy changes

