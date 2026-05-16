# Quality Gates

Quality gates determine whether work can move forward.

## Gate Matrix

| Gate | Required When | Evidence |
| --- | --- | --- |
| Requirement Review | Any new capability | Requirement or PRD reviewed |
| Design Review | Architecture, schema, workflow, security, or agent behavior changes | RFC or ADR |
| Unit Tests | Deterministic code | Passing tests |
| Integration Tests | Multiple modules interact | Passing integration workflow |
| Data Quality Check | Market/account data is used | Data validation report |
| Backtest | Strategy, signal, skill, or portfolio logic changes | Backtest report |
| Shadow Live | Candidate skill or agent decision workflow changes | Shadow portfolio report |
| Human Approval | Live trading, account-risk, or auto-promotion changes | Release approval |
| Rollback Plan | Any released behavior | Rollback instructions |

## Default Done Definition

A ticket is done only when:

- Scope matches the requirement.
- Tests or evals cover the main risk.
- Documentation is updated.
- CI passes.
- Remaining risk is documented.

## Investment Feature Done Definition

Investment features additionally require:

- Hypothesis and review ledger impact described.
- Benchmark comparison defined.
- Account-risk impact described.
- Promotion and rollback criteria defined.

