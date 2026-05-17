# SPEC-CI-0001 测试场景

## 场景 1：本地验证

- Given 本地仓库已经安装开发依赖。
- When 执行 `python -m harness_engine.cli validate`、`ruff check .` 和 `pytest`。
- Then 所有命令必须通过。

## 场景 2：远端 CI 验证

- Given 提交被推送到 GitHub。
- When GitHub Actions 触发。
- Then CI 必须执行 Harness 校验、lint 和测试。

## 场景 3：dashboard artifact

- Given CI 核心测试已经通过。
- When 执行 `python -m harness_engine.cli dashboard`。
- Then CI 必须生成并上传 `harness-dashboard` artifact。

## 场景 4：界面类需求进入开发前

- Given 新需求涉及投资 Agent 控制台或可视化交互。
- When 任务进入 roadmap 和 sprint。
- Then 任务必须包含 `prototype_review` 门禁，并在 `docs/prototypes/` 留存证据。
