# SPEC 驱动的 CI/CD Harness 流程

本文把 LobeHub `my-harness-workflow` skill 的 SPEC 工作流纳入本项目 CI/CD。该 skill 的核心思想是：先用 SPEC 固化需求和验收标准，再按计划执行实现，最后同步文档、进度和交付证据。

## 流程总览

```text
SPEC plan
  -> EARS 需求和验收标准
  -> plan.md 拆解里程碑
  -> scenarios.md 定义测试场景
  -> risks.md 记录风险和缓解
  -> run 阶段执行实现
  -> sync 阶段更新文档、面板、PR 或发布记录
```

本项目的落地目录：

```text
.moai/specs/<SPEC-ID>/
  spec.md
  plan.md
  scenarios.md
  risks.md
  progress.md
```

## EARS 需求格式

CI/CD 相关需求应尽量写成可验证语句：

- 普遍型：系统应当在每次 push 和 pull request 时运行 Harness 校验。
- 事件型：当 GitHub Actions 运行时，系统应当生成 dashboard artifact。
- 异常型：如果测试失败，系统应当阻止发布候选进入下一阶段。
- 状态型：当任务处于发布候选状态时，系统应当保留回滚和监控证据。
- 可选型：当 Figma 原型门禁适用时，系统应当检查原型评审记录。

## 验收标准格式

验收标准使用 `AC-<SPEC>-<序号>`：

```text
AC-CI-001: GitHub Actions 必须执行 validate、ruff 和 pytest。
  - Verification: 查看 .github/workflows/ci.yml 和 CI run。
  - Priority: P0
```

## 当前 CI/CD 门禁

当前 GitHub Actions 执行：

1. 安装 Python 包。
2. 初始化 Harness 基线产物。
3. 校验 Harness 产物。
4. 运行 lint。
5. 运行测试。
6. 生成可视化 dashboard。
7. 上传 `harness-dashboard` artifact。

## 与投资 Agent 的关系

投资 Agent 的 CI/CD 不只验证代码，还要验证工程治理证据：

- 需求是否被结构化记录。
- 是否完成 Figma 原型确认。
- 是否完成路线图和 sprint 拆解。
- 是否定义测试、回测、影子盘或人工审批门禁。
- 是否生成可视化面板，方便复盘开发状态和提交记录。

## 后续增强

- 使用 GitHub API 把 check run、PR、review 状态写入 `status.json`。
- 为每个 SPEC 自动生成 GitHub issue 或 project item。
- 将 dashboard 发布到 GitHub Pages。
- 为 shadow live 和生产发布增加手动审批环境。
