# Harness 任务拆解与可视化调研

本文记录主流 Harness、Agent 与工作流平台在“需求拆解、执行状态、测试门禁、可视化监控”上的实现模式，并给出本项目的落地方案。

## 主流实现模式

### GitHub Projects：状态字段驱动的任务看板

GitHub Projects 的核心做法是把 issue、PR、草稿项纳入统一项目视图，再通过字段、过滤器和视图组织工作。Board layout 适合表达“待办、开发中、评审中、完成”等状态，字段则用于表示负责人、优先级、里程碑、风险和迭代。

参考：https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-board-layout

可借鉴点：

- 把大需求拆成可独立交付的工作项。
- 每个工作项必须有状态字段，面板只做状态聚合和视图切换。
- 状态变更应尽量由工作流事件驱动，例如 PR 合并、CI 通过、评审完成。

### Harness CI/CD：流水线、阶段、步骤的可下钻视图

Harness 的 CI/CD 面板通常围绕 pipeline、stage、step 和 execution 展开，强调每次执行的状态、耗时、失败点、审批点和回滚路径。它不是单纯的任务列表，而是把“实现是否真的被验证”作为一等信息展示。

参考：

- https://developer.harness.io/docs/platform/dashboards/dashboard-standard/overview
- https://developer.harness.io/docs/continuous-integration/get-started/overview/

可借鉴点：

- 面板不只展示任务状态，也要展示门禁证据。
- 状态需要能追溯到测试、部署、审批、回滚等具体环节。
- 失败状态要能指向下一步动作，而不是只显示红色标记。

### LangGraph Studio：Agent 执行图与中间状态可视化

LangGraph Studio 面向 Agent 开发调试，重点是展示图结构、节点执行、状态变化和中间输出。它解决的是“Agent 为什么这样行动”的可解释性问题。

参考：https://docs.langchain.com/langgraph-platform/langgraph-studio

可借鉴点：

- Agent 任务应被拆成可观察节点，而不是只有最终回答。
- 每个节点保留输入、输出、状态和失败原因。
- 复盘时要能回看决策路径，尤其是投资假设、信号、风控和执行建议。

### Temporal / Prefect：工作流运行状态与历史追踪

Temporal Web UI 和 Prefect UI 都强调 workflow / flow run 的状态、历史、重试、失败原因和任务级别追踪。它们的共同点是把运行时状态持久化，使长流程可以恢复、审计和复盘。

参考：

- https://docs.temporal.io/web-ui
- https://docs.prefect.io/

可借鉴点：

- 长周期任务要有可查询的运行记录。
- 任务状态要保留历史，而不是只保留当前状态。
- 失败、重试、人工介入和恢复都应成为面板的一部分。

## 本项目落地方案

本项目先实现轻量、可提交到仓库的本地静态面板，再逐步接入 GitHub Projects、GitHub Actions、Harness Pipeline 或后续自研执行器。

### 数据模型

当前面板按以下层级聚合：

```text
需求 Requirement
  -> 路线图 Roadmap
  -> 任务 Ticket
  -> 门禁 Gate
  -> 测试 / 评审 / 发布证据
```

状态定义：

- `待拆解`：需求已记录，但还没有路线图。
- `待开发`：任务已拆解，但尚未进入 sprint 或缺少执行证据。
- `开发中`：任务进入 sprint，但仍有未通过门禁。
- `测试完成`：任务声明的门禁均已有证据。
- `门禁受阻`：高风险门禁缺失，需要补评估、影子盘、人工审批或回滚方案。

### 产物

- `docs/dashboard/status.json`：机器可读状态，可被 CI、GitHub Pages 或外部监控系统消费。
- `docs/dashboard/index.html`：静态看板，适合本地打开，也适合后续发布到 Pages。
- `python -m harness_engine.cli dashboard`：重新生成面板的标准入口。

### 后续增强

- 接入 GitHub Projects，把 `status.json` 同步为 issue / project field。
- 接入 GitHub Actions，把最近一次 CI 结果写入面板顶部。
- 为 Agent 运行轨迹增加 run ledger，展示每次投资分析、信号生成、复盘和 skill 晋升的节点状态。
- 为账户收益、回撤、命中率、换手、交易成本和风控违规增加趋势图。
- 增加“人工审批队列”，把真实交易、账户风险和 skill 晋升从普通开发任务中分离出来。
