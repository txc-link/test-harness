# Risk Control

Investment-agent work has risk beyond normal software defects.

## Risk Classes

| Class | Example | Minimum Control |
| --- | --- | --- |
| Account Risk | bad position sizing, unsafe auto-trade | human approval, rollback, risk budget |
| Data Risk | stale quotes, wrong corporate actions | data validation, source redundancy |
| Model Risk | hallucinated thesis, overconfident decision | structured evidence, review ledger |
| Strategy Risk | overfit factor, regime decay | out-of-sample backtest, shadow live |
| Operational Risk | failed scheduler, broken alerting | runbook, monitoring, retry policy |
| Compliance Risk | advice wording, user suitability | disclaimer, approval, audit trail |

## Required Controls

- Every live-impacting change has a risk owner.
- Every strategy/skill promotion has a rollback rule.
- Every account metric has a benchmark.
- Every agent recommendation is replayable from stored evidence.

