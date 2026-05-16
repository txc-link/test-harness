# Harness Skill Stack

These Codex skills are installed to support the investment-agent harness workflow.

## Project Skill

- `investment-agent-harness`: Project-specific workflow for requirements, decomposition, sprint planning, gates, CI/CD, and controlled evolution.

## Core Workflow Skills

- `dev-workflow`: Local harness workflow skill based on Intake -> Context Load -> Harness Plan -> Gated Execution -> Verification -> Review -> Handoff.
- `create-plan`: Composio planning skill for implementation planning before coding.
- `gh-fix-ci`: Debug and fix failing GitHub Actions checks.
- `webapp-testing`: Composio Playwright-based web application testing workflow.

## Mainstream Harness Skills

- `gstack`: General project/agent stack workflow from `garrytan/gstack`.
- `using-superpowers`: Superpowers workflow entrypoint from `obra/superpowers`.
- `everything-claude-code`: ECC core conventions from `affaan-m/everything-claude-code`.

## Everything Claude Code Installation

ECC source was downloaded to:

```text
D:\stock-agent\tools\everything-claude-code
```

Installed Codex-ready ECC skills from `.agents/skills/` into:

```text
C:\Users\DELL\.codex\skills
```

Installed skill count:

```text
33
```

Project-local Codex reference configuration was copied to:

```text
D:\stock-agent\investment-agent-harness\.codex\config.toml
D:\stock-agent\investment-agent-harness\.codex\AGENTS.ECC.md
D:\stock-agent\investment-agent-harness\.codex\agents\
```

Global `~/.codex/config.toml` was not overwritten.

ECC installed skills:

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

## Platform Integration Skills

- `connect`: Composio integration skill for connecting Codex to external apps.
- `notion-spec-to-implementation`: Convert Notion specs into implementation plans.
- `notion-research-documentation`: Notion-backed research/documentation workflows.
- `mcp-builder`: Build and evaluate MCP servers.

## Engineering Delivery Skills

- `gh-address-comments`: Address GitHub PR review comments.
- `gh-fix-ci`: Debug and fix failing GitHub Actions checks.
- `yeet`: Publish local changes to GitHub and open a draft PR.
- `playwright`: Browser-driven testing and verification.
- `playwright-interactive`: Interactive browser verification.
- `jupyter-notebook`: Notebook workflows for analysis and experiment artifacts.
- `cli-creator`: Turn repeated commands/scripts/API calls into reusable CLI tools.

## Safety And Governance Skills

- `security-threat-model`: Threat-model security-sensitive changes.
- `security-best-practices`: Apply secure engineering practices.
- `security-ownership-map`: Map security ownership and responsibility.

## Documentation And API Skills

- `openai-docs`: Use current OpenAI API/product documentation.
- `stop-slop`: Clean AI-sounding prose from docs and communication.

## Frontend And Design Skills

- `frontend-skill`: Local frontend quality skill for UI workflow, verification, and anti-generic-AI design checks.
- `figma`: General Figma workflows.
- `figma-use`: Use Figma context.
- `figma-implement-design`: Implement from Figma design.

## Harness Platform Skills

- `create-pipeline`: Generate Harness CI/CD pipeline YAML.
- `debug-pipeline`: Debug Harness pipeline failures.
- `run-pipeline`: Run and monitor Harness pipelines.
- `dora-metrics`: Fetch or reason about DORA metrics through Harness SEI.
- `manage-feature-flags`: Manage Harness feature flags.

## Multi-Agent Orchestration Tools

The npm package `@shpitdev/codexharness` was attempted. The package files were partially present under:

```text
C:\Users\DELL\AppData\Roaming\npm\node_modules\@shpitdev\codexharness
```

The global install timed out before linking Windows commands. Prefer `npx @shpitdev/codexharness ...` or run from Git Bash if using the bash entrypoints.

## Notes

- Restart Codex after installing new skills so the runtime picks them up.
- Some third-party skills contain UTF-8 punctuation that the system validation helper cannot read under Windows GBK. That is a validator encoding limitation, not necessarily an installation failure.
- For investment-agent work, prefer this order:

```text
dev-workflow
  -> investment-agent-harness
  -> gstack / using-superpowers when the user requests those workflows
  -> security-threat-model for risk-sensitive changes
  -> gh-fix-ci / gh-address-comments / yeet for GitHub delivery work
  -> playwright for UI or browser verification
```
