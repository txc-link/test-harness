# 投资 Agent Harness - 智能体工作指南

## 使命

本仓库负责建设和运行“可复盘、可测试、可审计、可自我进化”的投资 Agent 工程环境。它不是单纯业务代码仓库，而是 Harness 控制层：统一管理需求、拆解、排期、测试、CI/CD、评估门禁、风险控制和受控自我进化。

## 语言规则

- 面向人的文档必须使用中文，包括 `README.md`、`docs/`、`templates/`、PRD、RFC、ADR、测试计划、复盘报告、发布说明和运行手册。
- 代码注释和 docstring 必须使用中文，除非引用第三方 API、协议字段、错误原文或命令输出。
- 机器可读字段、枚举值、文件路径、命令、包名、类名、函数名和配置 key 可以保留英文。
- 新增文档不得出现无必要的中英混写；确需使用英文术语时，应优先给出中文解释。

## 必须遵循的工作流

对任何非平凡需求，必须按以下流程处理：

1. 先分类：需求、RFC、ADR、实现、测试、发布、事故或进化提案。
2. 将新的产品意图记录为 `docs/requirements/` 下的结构化需求。
3. 面向用户行为创建 PRD；涉及架构或工作流变更时创建 RFC。
4. 已接受的架构、安全或进化策略决策必须记录为 ADR。
5. 将批准范围拆解为 `docs/roadmap/` 下的里程碑和带门禁的任务。
6. 将近期工作放入 `docs/sprints/` 下的 sprint 计划。
7. 在声明完成前，必须定义测试、评估规格或评审门禁。
8. 完成前运行本地验证：

```powershell
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m harness_engine.cli validate
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m ruff check .
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest
```

## 项目阶段

- `Discovery`：原始想法、参考项目分析、开放问题。
- `Requirement`：结构化问题、目标用户、范围、非目标和验收标准。
- `PRD/RFC/ADR`：产品行为、技术提案和已接受决策。
- `Plan`：路线图、架构决策、里程碑、风险和门禁矩阵。
- `Sprint`：任务选择、退出标准、负责人和预期测试。
- `Build`：带测试和文档的实现。
- `Evaluate`：lint、单元测试、集成测试、投资评估和 shadow live 门禁。
- `Release`：变更记录、迁移说明、发布清单。
- `Evolve`：复盘失败、提出 skill/config 变更、门禁评估、晋升、监控和回滚。

## 必读参考

在进行重要规划或实现前，必须查阅：

- `docs/HARNESS_OPERATING_MODEL.md`
- `docs/QUALITY_GATES.md`
- `docs/DELIVERY_PIPELINE.md`
- `docs/RISK_CONTROL.md`

应优先使用 `templates/` 中的模板，不要临时发明格式。

## 投资专用门禁

- 任何实盘交易行为必须要求人工确认。
- 任何 skill 晋升必须通过 backtest 和 shadow live 门禁。
- 任何账户风险变更必须包含回滚标准。
- 每个推荐能力都必须写入假设 ledger 和复盘 ledger。
- 每个盈利能力结论都必须区分 benchmark beta、strategy contribution、agent contribution 和 user execution impact。

## 安全边界

- 默认不启用实盘自动交易。
- 没有证据时不得自动晋升策略或 skill。
- 不得把 LLM 自我反思当成改进已经有效的证据。
- 除非用户明确要求，不要修改四个参考项目。
- 除非用户另有要求，生成的 Harness 产物必须保存在本仓库内。

## 参考项目

相邻项目只作为参考，默认不要修改：

- `../aiagents-stock`
- `../TradingAgents-astock`
- `../RD-Agent`
- `../deer-flow`
