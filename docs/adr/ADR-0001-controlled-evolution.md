# ADR-0001: Controlled Offline Evolution

## Status

Accepted

## Context

The investment agent must improve from account results, failed hypotheses, user corrections, and strategy evaluations. Because investment decisions affect real capital, the agent must not freely rewrite live trading rules or promote strategies without evidence.

## Decision

Use a controlled offline evolution loop:

```text
runtime learning -> review attribution -> candidate skill/config generation -> backtest -> shadow-live -> human approval -> promotion -> rollback monitoring
```

## Consequences

- Runtime learning can update memory and examples.
- High-risk strategy changes require evaluation gates.
- Skill versions are promoted only with measurable improvement.
- Rollback is part of the lifecycle, not an afterthought.

