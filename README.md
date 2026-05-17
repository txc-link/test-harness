# 投资 Agent Harness

本仓库是用于建设“可复盘、可测试、可审计、可自我进化”的投资 Agent 的工程 Harness。

它与 `D:\stock-agent` 下的四个参考项目保持分离。参考项目提供 agent、量化、投研和流程灵感；本仓库负责把需求、拆解、开发、测试、CI/CD、评估、发布、复盘和自我进化治理串成一个可执行闭环。

```text
想法
  -> 需求摄入
  -> 发现与调研
  -> PRD/RFC/ADR
  -> 路线图
  -> sprint 计划
  -> 开发任务
  -> 测试与评估
  -> CI/CD
  -> 发布
  -> 监控
  -> 复盘
  -> 受控进化提案
```

## 快速开始

```powershell
cd D:\stock-agent\investment-agent-harness
python -m pip install -e .[dev]
iah init
iah develop-file docs\requirements\REQ-smoke-input.md --title "UTF8 Requirement Document Smoke Test"
iah validate
pytest
```

## 本仓库产出什么

- `docs/requirements/`：结构化需求和 PRD。
- `docs/roadmap/`：里程碑和任务拆解。
- `docs/sprints/`：可进入开发的 sprint 计划和任务。
- `docs/evals/`：盈利评估和自我进化评估规格。
- `docs/adr/`：架构、安全和策略决策记录。
- `docs/rfc/`：架构或流程提案。
- `docs/test-plans/`：测试计划。
- `docs/releases/`：发布清单。
- `docs/runbooks/`：可重复执行的运行手册。
- `docs/reviews/`、`docs/risks/`、`docs/incidents/`、`docs/metrics/`：复盘、风险、事故和指标记录。

## 核心文档

- [Harness 运行模型](docs/HARNESS_OPERATING_MODEL.md)
- [Harness 引擎](docs/HARNESS_ENGINE.md)
- [Harness 成熟度模型](docs/HARNESS_MATURITY_MODEL.md)
- [Agent 角色](docs/AGENT_ROLES.md)
- [质量门禁](docs/QUALITY_GATES.md)
- [交付流水线](docs/DELIVERY_PIPELINE.md)
- [风险控制](docs/RISK_CONTROL.md)
- [可观测性与指标](docs/OBSERVABILITY_METRICS.md)
- [CI/CD 方案](docs/CICD.md)
- [开发环境](docs/DEV_ENVIRONMENT.md)
- [Harness Skill 栈](docs/SKILL_STACK.md)
- [任务拆解与可视化调研](docs/HARNESS_DASHBOARD_RESEARCH.md)
- [可视化实施说明](docs/HARNESS_VISUALIZATION_GUIDE.md)
- [Figma 原型验证流程](docs/FIGMA_PROTOTYPE_WORKFLOW.md)
- [SPEC 驱动 CI/CD 流程](docs/SPEC_CICD_WORKFLOW.md)
- [编码规范](docs/CODING_GUIDELINES.md)

## 运行原则

1. 每条投资建议都必须成为可追踪的投资假设。
2. 每条假设都必须有期限、失效条件、基准和复盘路径。
3. Agent 改进只有通过评估门禁后才可信。
4. 影响真实账户的变化默认需要人工确认。
5. skills 必须版本化、可评估、可晋升、可回滚。

## 本地验证

```powershell
.\scripts\check.ps1
```

该命令会运行 Harness 校验、lint 和测试。
