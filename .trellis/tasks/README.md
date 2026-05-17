# Trellis 任务中心

本目录保存跨会话、跨 Agent 可交接的任务卡。

任务卡应使用 `templates/trellis_task.md` 创建，并包含：

- 任务目标。
- 需求、SPEC、原型、roadmap 和 sprint 上下文。
- Plan / Implement / Verify / Finish 四阶段记录。
- Finish 阶段需要回写到 `.trellis/spec/` 的经验。

创建命令：

```powershell
python -m harness_engine.cli new trellis-task "任务名称"
```
