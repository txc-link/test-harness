# RFC：UTF-8 需求文档 Smoke Test

## 状态

草稿

## 背景

中文需求如果只通过命令行参数输入，在部分 Windows 终端下可能出现显示或编码问题。Harness 需要支持直接读取 UTF-8 文档。

## 提案

使用 `develop-file` 命令从 UTF-8 文档读取需求正文，再生成结构化需求、roadmap、sprint、交付物和 flow report。

## 备选方案

- 继续只使用命令行参数：简单但更容易受终端编码影响。
- 接入外部文档系统：能力更强，但当前阶段复杂度过高。

## 影响系统

- Harness CLI。
- 需求摄入流程。
- 开发闭环报告。

## 数据和 Schema 变化

不新增 schema 字段。

## 评估与测试计划

- 增加 UTF-8 需求读取测试。
- 运行本地 `.\scripts\check.ps1`。

## 发布计划

随 Harness 文档和 CLI 一起发布。

## 回滚计划

保留原有 `develop` 命令；如 `develop-file` 失败，可回退到原命令。

## 开放问题

- 是否需要增加 Markdown frontmatter 支持？
