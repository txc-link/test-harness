# PRD：UTF-8 需求文档 Smoke Test

## 状态

草稿

## 问题

需要验证中文 UTF-8 需求文档可以稳定进入 Harness 工作流，并生成结构化需求、roadmap、sprint、开发交付物和测试证据。

## 目标用户

- Harness 维护者。
- 使用中文编写需求的产品和研发人员。

## 目标

- 从中文需求文档生成结构化需求。
- 生成可追踪的开发闭环证据。
- 保证本地校验和测试通过。

## 非目标

- 不验证实盘交易。
- 不接入真实市场数据。

## 用户工作流

1. 用户写入中文需求文档。
2. Harness 读取文档并生成需求产物。
3. Harness 生成 roadmap、sprint、ticket 和 test plan。
4. 用户运行检查并查看 flow report。

## 功能需求

- 支持 UTF-8 文档输入。
- 生成结构化 YAML 需求。
- 生成 markdown 交付物。
- 写入流程证据报告。

## 非功能需求

- 文档必须可读。
- 生成产物必须可被 schema 校验。

## 投资风险影响

该 smoke test 不影响投资账户和交易逻辑。

## 验收标准

- `develop-file` 能处理中文需求文档。
- `.\scripts\check.ps1` 通过。

## 开放问题

- 后续是否需要从 Obsidian 需求文档直接摄入？
