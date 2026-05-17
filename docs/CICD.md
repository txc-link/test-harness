# CI/CD 方案

## 当前 CI

GitHub Actions 工作流：

- `.github/workflows/ci.yml`

运行内容：

```text
python -m pip install -e .[dev]
python -m harness_engine.cli validate
ruff check .
pytest
```

## 本地等价命令

```powershell
.\scripts\check.ps1
```

## CD 策略

第一阶段没有生产部署目标。此时 CD 表示发布已经验证的规划产物和文档。

第二阶段应加入：

- 产物打包。
- 文档站点构建。
- schema 版本化发布。

第三阶段应加入：

- staging 部署。
- 迁移检查。
- shadow live worker 部署。
- 手动晋升审批。

## 必需发布门禁

- CI 通过。
- 新范围已经更新 `docs/requirements/`。
- 里程碑变化已经更新 `docs/roadmap/`。
- 投资评估变化已经更新 `docs/evals/`。
- 架构或安全策略变化已经新增 ADR。
