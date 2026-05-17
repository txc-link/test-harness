# 开发闭环报告：UTF-8 需求文档 Smoke Test

## 需求

- ID：REQ-0004
- 标题：UTF-8 需求文档 Smoke Test

## 拆解

- Roadmap 里程碑数量：5
- Sprint：SPRINT-0004
- Sprint 任务：T-0001, T-0002

## 已生成交付物

- `docs/requirements/REQ-0004.yaml`
- `docs/roadmap/REQ-0004-roadmap.yaml`
- `docs/sprints/SPRINT-0004.yaml`
- `docs/requirements/PRD-utf8-requirement-document-smoke-test.md`
- `docs/rfc/RFC-utf8-requirement-document-smoke-test.md`
- `docs/sprints/TICKET-utf8-requirement-document-smoke-test.md`
- `docs/test-plans/TEST-utf8-requirement-document-smoke-test.md`

## 任务门禁

| 任务 | 标题 | 风险 | 门禁 |
| --- | --- | --- | --- |
| T-0001 | 创建工程 Harness CLI 和产物目录 | low | requirement_review, unit_tests |
| T-0002 | 定义假设、计划、事件、结果和复盘 ledgers | medium | requirement_review, design_review, unit_tests |
| T-0003 | 构建账户和 Agent 盈利归因模型 | high | design_review, integration_tests, data_quality |
| T-0004 | 实现带晋升门禁的版本化 skill registry | high | unit_tests, backtest, shadow_live, human_approval, rollback_plan |
| T-0005 | 创建 shadow portfolio 评估闭环 | critical | integration_tests, data_quality, shadow_live, human_approval, rollback_plan |

## 验证命令

```powershell
.\scripts\check.ps1
```

## 退出标准

- CLI 的 intake、plan 和 validate 命令在本地通过。
- 初始 ledger 和 evolution specs 已完成评审。
- 单元测试通过。
