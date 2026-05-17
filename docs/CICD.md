# CI/CD 方案

## SPEC 驱动

CI/CD 变更必须优先写入 SPEC，再进入实现和同步。当前主 SPEC：

- `.moai/specs/SPEC-CI-0001/spec.md`
- `.moai/specs/SPEC-CI-0001/plan.md`
- `.moai/specs/SPEC-CI-0001/scenarios.md`
- `.moai/specs/SPEC-CI-0001/risks.md`
- `.moai/specs/SPEC-CI-0001/progress.md`

该结构来自 LobeHub `my-harness-workflow` skill：用 EARS 需求、验收标准、计划、测试场景、风险和进度文件组织 CI/CD 工作。

## 当前 CI

GitHub Actions 工作流：

- `.github/workflows/ci.yml`

运行内容：

```text
python -m pip install -e .[dev]
python -m harness_engine.cli init
python -m harness_engine.cli validate
ruff check .
pytest
python -m harness_engine.cli dashboard
upload harness-dashboard artifact
```

## 本地等价命令

```powershell
.\scripts\check.ps1
python -m harness_engine.cli dashboard
```

## CD 策略

第一阶段没有生产部署目标。此时 CD 表示发布已经验证的规划产物、文档和 dashboard artifact。

第二阶段应加入：

- 文档站点构建。
- dashboard 发布到 GitHub Pages。
- schema 版本化发布。
- GitHub API 状态同步。

第三阶段应加入：

- staging 部署。
- 迁移检查。
- shadow live worker 部署。
- 手动晋升审批。

## 必需发布门禁

- CI 通过。
- 新范围已经更新 `docs/requirements/`。
- 界面类需求已经完成 `docs/prototypes/` 原型评审。
- 里程碑变化已经更新 `docs/roadmap/`。
- 投资评估变化已经更新 `docs/evals/`。
- 架构或安全策略变化已经新增 ADR。
- dashboard artifact 已生成，可追溯提交、需求和任务状态。
