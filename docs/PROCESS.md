# Engineering Process

This harness makes the investment-agent project work like a small product and platform organization.

## 1. Intake

Raw ideas are converted into structured records:

- problem
- users
- outcomes
- scope
- non-goals
- risks
- acceptance criteria

Command:

```powershell
python -m harness_engine.cli intake "requirement text"
```

## 2. Discovery

Discovery answers:

- What user pain does this solve?
- What existing project or module can be reused?
- What data, model, account, or execution risk exists?
- What must be tested before release?

Discovery output can become a PRD, RFC, or both.

## 3. PRD / RFC / ADR

Use:

- `templates/prd.md` for product behavior.
- `templates/rfc.md` for architecture or workflow proposals.
- `docs/adr/` for accepted decisions.

## 4. Decomposition

Each approved requirement is decomposed into:

- milestones
- tickets
- risk level
- required gates
- deliverables

Command:

```powershell
python -m harness_engine.cli plan docs\requirements\REQ-0001.yaml
```

## 5. Scheduling

Sprint plans must include:

- goals
- ticket IDs
- start and end dates
- exit criteria

Sprint artifacts live in `docs/sprints/`.

## 6. Development Gates

Default gates:

- requirement review
- design review
- unit tests
- integration tests
- data quality check
- backtest
- shadow-live evaluation
- human approval
- rollback plan

Investment features choose gates by risk. UI-only documentation changes do not need backtest. Skill promotion, signal logic, portfolio logic, and trading rules do.

## 7. CI/CD

Current CI:

- install package
- initialize harness artifacts
- validate harness artifacts
- run lint
- run tests

CD is intentionally documentation/artifact-only until a real deploy target exists.

## 8. Release

Use `templates/release_checklist.md`. Releases require:

- green CI
- updated docs
- rollback plan
- monitoring plan
- risk review

## 9. Evolution

Evolution work must follow:

```text
runtime traces -> review attribution -> candidate change -> eval gate -> promotion -> monitoring -> rollback
```

Do not merge evolution proposals that lack metrics.

