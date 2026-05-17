# Harness 成熟度模型

Harness 应分级成熟。对高风险投资功能，不允许跳级。

## Level 0：临时协作

- 想法只在聊天中讨论。
- 代码直接修改。
- 测试可有可无。
- 决策和结果之间没有持久轨迹。

该级别不适合投资 Agent 工作。

## Level 1：可追踪计划

- 需求结构化。
- 存在 roadmap 和 sprint 计划。
- 基础 CI 能运行 lint 和测试。
- ADR 记录重要决策。

这是当前基础目标。

## Level 2：质量门禁交付

- 每个任务声明门禁。
- 高风险工作有测试计划。
- CI 阻止破坏性变更。
- 存在发布清单和回滚计划。

这是近期目标。

## Level 3：评估门禁 Agent 工作

- Agent 推荐被记录为投资假设。
- 账户 alpha 和 skill evolution 能被评估。
- shadow portfolio 对比 Agent、策略、用户和基准结果。
- skill 晋升必须依赖证据。

这是投资 Agent MVP 目标。

## Level 4：受控自我进化

- 运行轨迹进入复盘和学习流程。
- 候选 skill/config 在线下生成。
- backtest 和 shadow live 决定是否晋升。
- 回滚和漂移监控成为标准流程。

这是自我进化 Agent 目标。

## Level 5：治理化自治

- 低风险改进可以自动晋升。
- 高风险变更需要审批。
- 发布、监控和回滚自动化。
- 定期评审治理指标。

这是长期目标。
