# Harness Skill 栈

以下 Codex skills 用于支撑投资 Agent Harness 工作流。

## 项目专用 Skill

- `investment-agent-harness`：本项目专用工作流，覆盖需求、拆解、sprint 计划、门禁、CI/CD 和受控进化。

## 核心工作流 Skills

- `dev-workflow`：本地 Harness 工作流，覆盖 Intake -> Context Load -> Harness Plan -> Gated Execution -> Verification -> Review -> Handoff。
- `create-plan`：在编码前生成实现计划。
- `gh-fix-ci`：调试和修复失败的 GitHub Actions。
- `webapp-testing`：基于 Playwright 的 Web 应用测试工作流。

## 主流 Harness Skills

- `gstack`：来自 `garrytan/gstack` 的通用项目和 Agent 栈工作流。
- `using-superpowers`：来自 `obra/superpowers` 的工作流入口。
- `everything-claude-code`：来自 `affaan-m/everything-claude-code` 的核心约定。
- `Trellis`：来自 `mindfold-ai/Trellis` 的共享规格、任务中心、workspace journal 和 Plan / Implement / Verify / Finish 回写思想；本项目已融合到 `.trellis/` 目录和统一 Harness 工作流。

## Everything Claude Code 安装情况

ECC 源码下载位置：

```text
D:\stock-agent\tools\everything-claude-code
```

已将 `.agents/skills/` 中 Codex 可用 skills 安装到：

```text
C:\Users\DELL\.codex\skills
```

安装数量：

```text
33
```

项目本地 Codex 参考配置复制到：

```text
D:\stock-agent\investment-agent-harness\.codex\config.toml
D:\stock-agent\investment-agent-harness\.codex\AGENTS.ECC.md
D:\stock-agent\investment-agent-harness\.codex\agents\
```

没有覆盖全局 `~/.codex/config.toml`。

## 已安装 ECC skills

```text
agent-introspection-debugging
agent-sort
api-design
article-writing
backend-patterns
brand-voice
bun-runtime
coding-standards
content-engine
crosspost
deep-research
dmux-workflows
documentation-lookup
e2e-testing
eval-harness
everything-claude-code
exa-search
fal-ai-media
frontend-patterns
frontend-slides
investor-materials
investor-outreach
market-research
mcp-server-patterns
mle-workflow
nextjs-turbopack
product-capability
security-review
strategic-compact
tdd-workflow
verification-loop
video-editing
x-api
```

## 平台集成 Skills

- `connect`：将 Codex 连接到外部应用。
- `notion-spec-to-implementation`：将 Notion 需求转成实现计划。
- `notion-research-documentation`：基于 Notion 的研究和文档工作流。
- `mcp-builder`：构建和评估 MCP server。

## 工程交付 Skills

- `gh-address-comments`：处理 GitHub PR review 评论。
- `gh-fix-ci`：调试并修复失败的 GitHub Actions。
- `yeet`：发布本地变更到 GitHub 并打开 draft PR。
- `playwright`：浏览器驱动的测试和验证。
- `playwright-interactive`：交互式浏览器验证。
- `jupyter-notebook`：分析和实验 notebook 工作流。
- `cli-creator`：将重复命令、脚本或 API 调用转成可复用 CLI。

## 安全与治理 Skills

- `security-threat-model`：为敏感变更建模威胁。
- `security-best-practices`：应用安全工程实践。
- `security-ownership-map`：映射安全责任和归属。

## 文档与 API Skills

- `openai-docs`：使用最新 OpenAI API 和产品文档。
- `stop-slop`：清理文档和沟通中的 AI 腔。

## 前端与设计 Skills

- `frontend-skill`：本地前端质量 skill，覆盖 UI 工作流、验证和反泛化 AI 设计检查。
- `figma`：通用 Figma 工作流。
- `figma-use`：使用 Figma 上下文。
- `figma-implement-design`：从 Figma 设计实现代码。

## Harness 平台 Skills

- `create-pipeline`：生成 Harness CI/CD pipeline YAML。
- `debug-pipeline`：调试 Harness pipeline 失败。
- `run-pipeline`：运行和监控 Harness pipeline。
- `dora-metrics`：通过 Harness SEI 获取或分析 DORA 指标。
- `manage-feature-flags`：管理 Harness feature flags。

## 多 Agent 编排工具

曾尝试安装 npm 包 `@shpitdev/codexharness`。包文件部分存在于：

```text
C:\Users\DELL\AppData\Roaming\npm\node_modules\@shpitdev\codexharness
```

全局安装在链接 Windows 命令前超时。需要使用时，优先尝试 `npx @shpitdev/codexharness ...`，或在 Git Bash 中运行 bash 入口。

## 备注

- 安装新 skills 后应重启 Codex，让运行时加载它们。
- 部分第三方 skills 包含 UTF-8 标点，Windows GBK 下的系统验证辅助工具可能无法读取。这是验证器编码限制，不一定代表安装失败。
- 投资 Agent 工作优先按以下顺序选择能力：

```text
dev-workflow
  -> investment-agent-harness
  -> 用户指定时使用 gstack / using-superpowers
  -> 风险敏感变更使用 security-threat-model
  -> GitHub 交付使用 gh-fix-ci / gh-address-comments / yeet
  -> UI 或浏览器验证使用 playwright
```
