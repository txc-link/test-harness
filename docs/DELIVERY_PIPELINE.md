# Delivery Pipeline

## Local Pipeline

```text
bootstrap -> validate artifacts -> lint -> test -> package check
```

Command:

```powershell
.\scripts\check.ps1
```

## Pull Request Pipeline

```text
schema/artifact validation
  -> lint
  -> unit tests
  -> integration tests when present
  -> eval smoke tests when present
  -> review
```

## Release Pipeline

```text
release branch
  -> freeze scope
  -> run full validation
  -> generate release notes
  -> review rollback plan
  -> tag release
  -> deploy docs/artifacts
  -> monitor
```

## Environment Strategy

| Environment | Purpose | Allowed Behavior |
| --- | --- | --- |
| local | Development | No live trading |
| test | CI validation | Synthetic fixtures only |
| staging | Integration and dry runs | Paper trading only |
| shadow_live | Real market data, no execution | Shadow portfolios only |
| production | User-facing operation | Human-gated trading only |

