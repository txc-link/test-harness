# 投资 Ledger Schemas

产品必须为每个决策保留可回放的审计轨迹。

## Hypothesis Ledger

```yaml
hypothesis_id: H-0001
symbol: 600519
market: CN_A
created_at: 2026-05-16T20:00:00+08:00
direction: bullish
confidence: 0.72
horizon_days: 20
thesis: "资金面和基本面共振，未来 20 个交易日可能有超额收益机会。"
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

## Alert Ledger

```yaml
alert_id: A-0001
symbol: 600519
market: CN_A
triggered_at: 2026-05-16T10:30:00+08:00
severity: watch
rule: price_breakout
reason: "价格突破近 20 日高点，成交量同步放大。"
recommended_action: review_hypothesis
expires_at: 2026-05-17T15:00:00+08:00
status: open
```

## Evolution Ledger

```yaml
evolution_id: EV-0001
skill_id: earnings-event-analysis
candidate_version: 0.2.0
source: review_failure_mode
hypothesis: "加强财报异常项识别可以降低事件解读误报率。"
required_gates:
  - backtest
  - shadow_live
  - human_approval
rollback_rule: "shadow live 误报率高于当前 active 版本时回滚。"
status: candidate
```
