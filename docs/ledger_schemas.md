# Investment Ledger Schemas

The product must preserve a replayable audit trail for every decision.

## Hypothesis Ledger

```yaml
hypothesis_id: H-0001
symbol: 600519
market: CN_A
created_at: 2026-05-16T20:00:00+08:00
direction: bullish
confidence: 0.72
horizon_days: 20
thesis: "资金和基本面共振，未来 20 个交易日有超额收益机会。"
evidence: []
invalid_if: []
benchmark: CSI300
status: open
```

## Trade Plan Ledger

```yaml
plan_id: P-0001
hypothesis_id: H-0001
action: watch_or_buy
entry_zone: []
stop_loss: null
take_profit: []
position_size_pct: 5
requires_human_approval: true
```

## Review Ledger

```yaml
review_id: R-0001
hypothesis_id: H-0001
reviewed_at: 2026-06-15T15:30:00+08:00
return_1d: null
return_5d: null
return_20d: null
benchmark_excess_return: null
outcome: pending
failure_modes: []
lessons: []
skill_update_candidates: []
```

