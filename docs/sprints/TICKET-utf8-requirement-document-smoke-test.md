# 任务：UTF-8 需求文档 Smoke Test

## 关联需求

REQ-0004

## 问题

需要验证中文 UTF-8 需求文档可以稳定进入 Harness 工作流。

## 范围

- 读取 UTF-8 需求文档。
- 生成结构化需求、roadmap、sprint、PRD、RFC、ticket、test plan。
- 生成 flow report。

## 范围外

- 不接入真实市场数据。
- 不执行实盘交易。

## 交付物

- `docs/requirements/REQ-0004.yaml`
- `docs/roadmap/REQ-0004-roadmap.yaml`
- `docs/sprints/SPRINT-0004.yaml`
- flow report

## 门禁

- [x] 需求评审
- [x] 单元测试
- [x] 本地 CI 检查

## 验收标准

- 本地检查通过。
- 中文需求文本可以按 UTF-8 读取。

## 风险

- Windows 终端显示可能乱码，但文件本身必须保持 UTF-8。

## 备注

该任务是 Harness 工作流 smoke test。
