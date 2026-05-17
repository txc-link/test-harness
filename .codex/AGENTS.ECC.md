# Codex CLI 的 ECC 补充说明

本文档补充根目录 `AGENTS.md`，用于说明 Codex/ECC 相关约定。

## 模型建议

| 任务类型 | 建议模型 |
| --- | --- |
| 常规编码、测试、格式化 | GPT 5.4 |
| 复杂功能、架构设计 | GPT 5.4 |
| 调试、重构 | GPT 5.4 |
| 安全评审 | GPT 5.4 |

## Skills 发现

Skills 从 `.agents/skills/` 自动加载。每个 skill 通常包含：

- `SKILL.md`：详细说明和工作流。
- `agents/openai.yaml`：Codex 接口元数据。

常用 skills：

- `tdd-workflow`：测试驱动开发。
- `security-review`：安全检查清单。
- `coding-standards`：通用编码标准。
- `frontend-patterns`：React/Next.js 模式。
- `e2e-testing`：Playwright 端到端测试。
- `eval-harness`：评估驱动开发。
- `verification-loop`：构建、测试、lint、类型检查和安全检查。
- `deep-research`：多源研究。
- `dmux-workflows`：多 Agent 编排。

## MCP Servers

项目本地 `.codex/config.toml` 是 ECC 的默认 Codex 基线。当前基线启用 GitHub、Context7、Exa、Memory、Playwright 和 Sequential Thinking。更重的扩展只应在任务真正需要时放入 `~/.codex/config.toml`。

ECC 的规范 Codex section 名称是 `[mcp_servers.context7]`。启动包仍是 `@upstash/context7-mcp`。

## 外部操作边界

联网工具默认按只读方式使用。可以在用户请求范围内搜索、检查和起草；但发布、推送、合并、打开付费任务、派发远程 Agent、修改第三方资源或改动凭据前，必须获得明确授权。

当授权不清晰时，先生成本地计划或草稿，不直接执行外部动作。除非用户明确要求，不要修改用户配置和私有状态。

## 多 Agent 支持

Codex 支持通过 `features.multi_agent` 使用多 Agent 工作流。

- 在 `.codex/config.toml` 中通过 `[features] multi_agent = true` 启用。
- 在 `[agents.<name>]` 下定义项目本地角色。
- 每个角色指向 `.codex/agents/` 下的 TOML 配置。
- 在 Codex CLI 中使用 `/agent` 查看和引导子 Agent。

本仓库示例角色：

- `.codex/agents/explorer.toml`：只读证据收集。
- `.codex/agents/reviewer.toml`：正确性和安全评审。
- `.codex/agents/docs-researcher.toml`：文档和 API 研究。
