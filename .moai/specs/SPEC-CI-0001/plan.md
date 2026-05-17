# SPEC-CI-0001 实施计划

## M1 基础校验

- 确认 CI 执行 `validate`、`ruff check .` 和 `pytest`。
- 保持本地命令与远端 CI 等价。

## M2 面板产物

- 在 CI 中生成 `docs/dashboard/index.html`。
- 在 CI 中生成 `docs/dashboard/status.json`。
- 上传 `harness-dashboard` artifact。

## M3 SPEC 化治理

- 建立 `.moai/specs/SPEC-CI-0001/` 目录。
- 按 `spec.md`、`plan.md`、`scenarios.md`、`risks.md`、`progress.md` 组织证据。
- 使用 `AC-CI-*` 验收标准追踪 CI/CD 变更。

## M4 后续集成

- 接入 GitHub API 写入 check run 和 PR 状态。
- 发布 dashboard 到 GitHub Pages。
- 为 staging、shadow live 和 production 增加审批环境。
