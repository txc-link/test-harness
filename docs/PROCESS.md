# 工程流程

本 Harness 让投资 Agent 项目像一个小型产品和平台组织一样运行。

## 1. 需求摄入

原始想法会被转换为结构化记录：

- 问题。
- 用户。
- 预期结果。
- 范围。
- 非目标。
- 风险。
- 验收标准。

命令：

```powershell
python -m harness_engine.cli intake "需求文本"
```

## 2. 调研发现

调研需要回答：

- 这个需求解决什么用户痛点？
- 哪个已有项目或模块可以复用？
- 存在哪些数据、模型、账户或执行风险？
- 发布前必须测试什么？

调研结果可以进入 PRD、RFC，或两者同时进入。

## 3. PRD / RFC / ADR

使用：

- `templates/prd.md` 描述产品行为。
- `templates/rfc.md` 描述架构或工作流提案。
- `docs/adr/` 记录已接受决策。

## 4. Figma 原型确认

凡是涉及界面、控制台、盯盘、告警、分析、复盘、回测、审批队列或可视化交互的需求，必须在排期开发前完成原型确认。

标准顺序：

```text
需求 / PRD
  -> Figma 原型
  -> 人工确认
  -> 需求回写
  -> roadmap 拆解
  -> sprint 排期
  -> 开发实现
```

原型确认必须记录在 `docs/prototypes/`，并说明：

- Figma 原型链接或截图。
- 人工确认结论。
- 需求、范围或交互路径的调整。
- 是否允许进入排期开发。

命令：

```powershell
python -m harness_engine.cli new prototype "投资 Agent 控制台原型评审"
```

## 5. 拆解

每个已批准需求都要拆解为：

- 里程碑。
- 任务。
- 风险等级。
- 必需门禁。
- 交付物。

界面类任务必须包含 `prototype_review` 门禁。原型确认导致需求变化时，必须先更新需求和 PRD/RFC，再生成或调整路线图。

命令：

```powershell
python -m harness_engine.cli plan docs\requirements\REQ-0001.yaml
```

## 6. Trellis 任务化

当任务需要跨会话、多人或多 Agent 协作时，必须建立 Trellis 上下文：

- `.trellis/spec/`：保存长期共享规则和经验。
- `.trellis/tasks/`：保存可交接任务卡。
- `.trellis/workspaces/`：保存大任务工作区上下文。
- `.trellis/journal/`：保存会话日志和 Finish 回写。

标准阶段：

```text
Plan -> Implement -> Verify -> Finish
```

Finish 阶段必须把可复用经验回写到 `.trellis/spec/`，并根据需要更新需求、SPEC、roadmap、sprint 或复盘记录。

命令：

```powershell
python -m harness_engine.cli new trellis-task "盯盘告警控制台"
python -m harness_engine.cli new trellis-journal "盯盘告警控制台开发日志"
```

## 7. 排期

Sprint 计划必须包含：

- 目标。
- 任务 ID。
- 开始和结束日期。
- 退出标准。

Sprint 产物保存在 `docs/sprints/`。

## 8. 开发门禁

默认门禁：

- requirement review。
- prototype review。
- design review。
- unit tests。
- integration tests。
- data quality check。
- backtest。
- shadow live evaluation。
- human approval。
- rollback plan。

投资功能按风险选择门禁。纯 UI 或文档变化不需要 backtest；但界面类需求必须有 prototype review。skill 晋升、信号逻辑、组合逻辑和交易规则必须需要 backtest。

## 9. CI/CD

当前 CI：

- 安装包。
- 初始化 Harness 产物。
- 校验 Harness 产物。
- 运行 lint。
- 运行测试。

在真实部署目标出现前，CD 只发布文档和规划产物。

## 10. 发布

使用 `templates/release_checklist.md`。发布需要：

- CI 通过。
- 文档更新。
- 回滚计划。
- 监控计划。
- 风险评审。

## 11. 进化

进化工作必须遵循：

```text
运行轨迹 -> 复盘归因 -> 候选变更 -> 评估门禁 -> 晋升 -> 监控 -> 回滚
```

缺少指标的进化提案不得合并。
