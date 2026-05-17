# 测试计划：UTF-8 需求文档 Smoke Test

## 范围

验证中文 UTF-8 需求文档可以进入 Harness 开发闭环。

## 被验证的风险

- Windows 终端编码导致中文需求不可读。
- 生成产物不符合 schema。
- 开发闭环无法端到端运行。

## 测试层级

- 单元测试。
- Harness schema 校验。
- 本地 CI 检查。

## Fixtures

- `docs/requirements/REQ-smoke-input.md`

## 用例

| 用例 | 输入 | 预期结果 |
| --- | --- | --- |
| UTF-8 文档摄入 | 中文 Markdown 需求 | 生成 `REQ-0004.yaml` |
| 开发闭环 | `develop-file` 命令 | 生成 roadmap、sprint、交付物和 flow report |
| 本地验证 | `.\scripts\check.ps1` | lint 和测试通过 |

## 退出标准

- Harness validation passed。
- ruff 通过。
- pytest 通过。
