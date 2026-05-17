# SPEC-CI-0001 风险记录

## R1：dashboard 产物含时间戳

- 风险：CI 中直接检查工作区 diff 会因为时间戳变化导致误报。
- 缓解：CI 只生成并上传 artifact，不要求生成物与仓库提交完全一致。

## R2：LobeHub token 可能失效

- 风险：market CLI 搜索或后续评分可能因为 token 失效失败。
- 缓解：已安装 skill 的 `SKILL.md` 保存在 `.agents/skills/`；项目流程不依赖运行时访问 LobeHub。

## R3：agentskillexchange skill 不存在

- 风险：指定的 `harness-ci-cd-platform` 未在 `agentskillexchange/skills` 中发现。
- 缓解：记录安装失败原因，并使用已安装的 SPEC workflow skill 完善本项目 CI/CD。

## R4：CI/CD 过早绑定生产发布

- 风险：投资 Agent 尚未有生产部署目标，过早接入生产 CD 会扩大风险。
- 缓解：当前 CD 仅发布验证后的文档、dashboard 和规划产物；真实交易相关发布必须走人工审批。
