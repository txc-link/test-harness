# Harness 运行模型

本仓库是投资 Agent 项目的控制平面。它不只是代码仓库，而是把产品意图、工程任务、测试、发布门禁、投资评估和受控自我进化连接起来的工作系统。

## 端到端流程

```text
想法
  -> 需求摄入
  -> 调研发现
  -> PRD
  -> RFC（涉及架构或流程变化时）
  -> ADR（接受决策后）
  -> roadmap 拆解
  -> sprint 排期
  -> 实现
  -> 测试与评估
  -> CI
  -> 发布候选
  -> 分阶段发布
  -> 监控
  -> 复盘
  -> 进化提案
```

## 工作项类型

| 类型 | 位置 | 用途 |
| --- | --- | --- |
| 需求 | `docs/requirements/` | 描述用户问题、范围和验收标准 |
| PRD | `docs/requirements/` | 描述产品行为和用户工作流 |
| RFC | `docs/rfc/` | 描述架构或工作流提案 |
| ADR | `docs/adr/` | 记录已接受的架构或策略决策 |
| Roadmap | `docs/roadmap/` | 拆解里程碑和工程任务 |
| Sprint | `docs/sprints/` | 近期交付计划 |
| 测试计划 | `docs/test-plans/` | 描述风险验证方式 |
| 评估规格 | `docs/evals/` | 描述投资或 Agent 质量评估 |
| 发布 | `docs/releases/` | 发布清单和说明 |
| 复盘 | `docs/reviews/` | sprint、事故或模型复盘 |
| 风险 | `docs/risks/` | 风险登记和缓解措施 |
| 运行手册 | `docs/runbooks/` | 可重复执行的运维步骤 |

## 生命周期状态

任务、评估和发布默认使用：

```text
draft -> reviewed -> approved -> in_progress -> validating -> ready -> released -> monitored -> retired
```

自我进化 skill 使用：

```text
candidate -> backtested -> shadow_live -> approved -> active -> monitored -> retired
```

## 决策规则

- 影响系统架构时，必须创建 RFC。
- RFC 被接受后，必须记录 ADR。
- 影响账户风险时，必须创建或更新评估规格。
- 影响实盘交易时，必须要求人工审批并提供回滚标准。
- 影响 skill 自我进化时，必须要求 backtest 和 shadow live 门禁。
