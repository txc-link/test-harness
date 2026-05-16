# Harness Engine

The Harness Engine is the local control plane for this project. It converts goals into durable artifacts, validates the engineering environment, and reports maturity.

## Commands

```powershell
python -m harness_engine.cli init
python -m harness_engine.cli intake "requirement text"
python -m harness_engine.cli plan docs\requirements\REQ-0001.yaml
python -m harness_engine.cli develop "requirement text" --title "Harness Status Command"
python -m harness_engine.cli develop-file docs\requirements\REQ-smoke-input.md --title "Harness Status Command"
python -m harness_engine.cli new rfc "Harness Control Plane"
python -m harness_engine.cli status
python -m harness_engine.cli status --write
python -m harness_engine.cli maturity
python -m harness_engine.cli validate
```

## Artifact Scaffolding

Supported `new` kinds:

```text
prd
rfc
ticket
test-plan
evolution
release
postmortem
risk-register
runbook
```

## Development Flow

`develop` is the smallest runnable Harness loop:

1. Capture the raw requirement text or UTF-8 requirement document as `docs/requirements/REQ-*.yaml`.
2. Decompose it into `docs/roadmap/REQ-*-roadmap.yaml`.
3. Create the first sprint as `docs/sprints/SPRINT-*.yaml`.
4. Scaffold PRD, RFC, ticket, and test-plan documents.
5. Write a flow evidence report in `docs/reviews/FLOW-*.md`.
6. Run schema validation before returning generated paths.

## Control Plane Responsibilities

- Keep project workflow artifacts discoverable.
- Keep quality gates explicit.
- Make maturity visible.
- Keep evolution proposals tied to evidence.
- Avoid uncontrolled changes to trading, account-risk, and skill promotion behavior.
