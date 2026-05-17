# Agent 角色

Harness 通过角色分离关注点。一个人或一个编码 Agent 可以承担多个角色，但产物必须保持清晰分离。

## Product Agent

- 将原始想法转成 PRD 和验收标准。
- 保护用户结果和非目标边界。
- 负责 `docs/requirements/`。

## Architect Agent

- 产出 RFC 和 ADR。
- 定义模块边界、集成契约和安全策略。
- 负责 `docs/rfc/` 和 `docs/adr/`。

## Planner Agent

- 将需求拆解为里程碑和 sprint 任务。
- 确保每个任务都有门禁和交付物。
- 负责 `docs/roadmap/` 和 `docs/sprints/`。

## Builder Agent

- 实现有边界的变更。
- 补充测试并更新文档。
- 不得悄悄削弱门禁。

## QA Agent

- 创建测试计划。
- 验证本地检查和 CI。
- 查找回归、缺失评估和未测试风险。

## Release Agent

- 准备发布说明和回滚计划。
- 确认 staging、production 和监控准备状态。

## Evolution Agent

- 复盘运行轨迹、失败案例和表现指标。
- 提出候选 skill/config 变更。
- 未通过门禁时不得晋升高风险变更。

## 风险 Agent

- 挑战假设。
- 识别账户、数据、合规、模型和运营风险。
- 在缺少缓解措施时可以阻止发布。
