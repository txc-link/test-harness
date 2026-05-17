# 质量门禁

质量门禁决定工作是否可以进入下一阶段。投资 Agent 的门禁不仅覆盖软件质量，也覆盖数据、模型、策略和账户风险。

## 门禁矩阵

| 门禁 | 何时需要 | 证据 |
| --- | --- | --- |
| Requirement Review | 任意新能力 | 已评审的需求或 PRD |
| Prototype Review | 界面、控制台、盯盘、告警、分析、复盘、审批队列或可视化交互变化 | Figma 原型链接、截图和人工确认记录 |
| Design Review | 架构、schema、工作流、安全或 Agent 行为变化 | RFC 或 ADR |
| Unit Tests | 确定性代码 | 通过的单元测试 |
| Integration Tests | 多模块交互 | 通过的集成流程 |
| Data Quality Check | 使用市场或账户数据 | 数据质量报告 |
| Backtest | 策略、信号、skill 或组合逻辑变化 | 回测报告 |
| Shadow Live | 候选 skill 或 Agent 决策流变化 | shadow portfolio 报告 |
| Human Approval | 实盘交易、账户风险或自动晋升变化 | 发布审批记录 |
| Rollback Plan | 任意发布行为 | 回滚说明 |

## 默认完成定义

任务只有同时满足以下条件才算完成：

- 范围与需求一致。
- 涉及界面时，Figma 原型已经人工确认，并且确认结论已经回写到需求和排期。
- 测试或评估覆盖主要风险。
- 文档已经更新。
- CI 通过。
- 剩余风险已经记录。

## 投资功能完成定义

投资相关功能还必须满足：

- 描述对 hypothesis ledger 和 review ledger 的影响。
- 定义基准比较方式。
- 描述账户风险影响。
- 定义晋升和回滚标准。
