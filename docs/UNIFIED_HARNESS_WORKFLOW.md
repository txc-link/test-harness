# 统一 Harness 工作流

本文融合 Trellis、SPEC 工作流、Figma 原型验证、gstack / Codex 评审习惯、Everything Claude Code 的工程约定，以及本项目已有投资 Agent Harness 要求，形成统一开发闭环。

## 融合原则

- Trellis 提供上下文骨架：共享规格、任务中心、工作区日志、Finish 回写。
- SPEC 提供验收骨架：EARS 需求、验收标准、计划、场景、风险、进度。
- Figma 提供界面验证：先原型、人工确认、需求回写，再排期开发。
- CI/CD 提供自动验证：Harness 校验、lint、测试、dashboard artifact。
- Dashboard 提供状态可视化：需求、任务、门禁、提交记录和测试状态。
- 投资 Agent 约束提供安全边界：回测、影子盘、人工审批和回滚。

## 端到端流程

```text
1. 需求讨论
   -> 捕获用户目标、投资场景、风险边界和开放问题

2. 文档生成
   -> docs/requirements/
   -> PRD / RFC / ADR
   -> 必要时创建 .moai/specs/<SPEC-ID>/

3. 原型设计
   -> 界面类需求生成或评审 Figma 原型
   -> docs/prototypes/ 记录人工确认
   -> 回写需求、范围和排期

4. Trellis 任务化
   -> .trellis/spec/ 保存长期规则和经验
   -> .trellis/tasks/ 保存可交接任务卡
   -> .trellis/workspaces/ 保存大任务工作上下文
   -> .trellis/journal/ 保存会话日志

5. 排期开发
   -> docs/roadmap/ 拆解里程碑
   -> docs/sprints/ 选择近期任务
   -> 每个任务声明门禁和验证方式

6. 实现
   -> 小步提交
   -> 优先简单、可读、可测试
   -> 不改变无关文件

7. 自动测试
   -> validate
   -> lint
   -> pytest
   -> 必要时浏览器验证、回测、影子盘验证

8. CI/CD 与可视化
   -> GitHub Actions 执行验证
   -> 生成 dashboard
   -> 上传 dashboard artifact
   -> 面板展示提交、需求、任务和门禁状态

9. Finish
   -> 复盘结果
   -> 将可复用经验写回 .trellis/spec/
   -> 更新 SPEC progress
   -> 生成后续任务
```

## 目录分工

| 目录 | 作用 |
| --- | --- |
| `docs/requirements/` | 需求和 PRD |
| `docs/rfc/` | 架构、流程和技术方案 |
| `docs/adr/` | 已接受决策 |
| `docs/prototypes/` | Figma 原型评审和人工确认 |
| `.moai/specs/` | EARS 需求、验收标准、计划、场景、风险和进度 |
| `.trellis/spec/` | 长期共享规则和经验 |
| `.trellis/tasks/` | 可交接任务卡 |
| `.trellis/workspaces/` | 大任务工作上下文 |
| `.trellis/journal/` | 会话日志和 Finish 回写入口 |
| `docs/roadmap/` | 里程碑和任务拆解 |
| `docs/sprints/` | 近期排期 |
| `docs/evals/` | 投资评估和进化评估 |
| `docs/dashboard/` | 可视化状态面板 |

## 任务状态机

Trellis 任务卡必须显式经历 `Plan -> Implement -> Verify -> Finish` 四个阶段。

```text
discussion
  -> documented
  -> prototyped（界面类需求）
  -> planned
  -> scheduled
  -> implementing
  -> verifying
  -> reviewed
  -> finished
  -> learned
```

`learned` 表示 Finish 阶段已经完成经验回写。对投资 Agent 来说，没有经验回写的任务不算真正完成，只能算交付了一个变更。

## 使用示例

创建共享规格：

```powershell
python -m harness_engine.cli new trellis-spec "投资 Agent 风控界面规则"
```

创建任务卡：

```powershell
python -m harness_engine.cli new trellis-task "盯盘告警控制台"
```

创建工作日志：

```powershell
python -m harness_engine.cli new trellis-journal "盯盘告警控制台开发日志"
```

生成面板：

```powershell
python -m harness_engine.cli dashboard
```

## 完成定义

一个需求只有同时满足以下条件，才算完成：

- 需求、范围和验收标准已经记录。
- 界面类需求已经完成 Figma 原型确认。
- 复杂或跨阶段工作已经建立 SPEC。
- 任务已经进入 roadmap 和 sprint。
- 实现有测试、评估或人工评审证据。
- CI 通过。
- dashboard 能展示状态和对应提交。
- Finish 阶段已经把可复用经验写回 `.trellis/spec/`。
