# Harness 引擎

Harness 引擎是本项目的本地控制平面。它把目标转成持久化产物，校验工程环境，并报告 Harness 成熟度。

## 命令

```powershell
python -m harness_engine.cli init
python -m harness_engine.cli intake "需求文本"
python -m harness_engine.cli plan docs\requirements\REQ-0001.yaml
python -m harness_engine.cli develop "需求文本" --title "Harness 状态命令"
python -m harness_engine.cli develop-file docs\requirements\REQ-smoke-input.md --title "Harness 状态命令"
python -m harness_engine.cli new rfc "Harness 控制平面"
python -m harness_engine.cli status
python -m harness_engine.cli status --write
python -m harness_engine.cli maturity
python -m harness_engine.cli validate
```

## 产物脚手架

`new` 支持的类型：

```text
prd
rfc
ticket
test-plan
evolution
release
postmortem
risk-register
runbook
```

## 开发闭环

`develop` 和 `develop-file` 是最小可运行 Harness 闭环：

1. 将原始需求文本或 UTF-8 需求文档记录为 `docs/requirements/REQ-*.yaml`。
2. 拆解为 `docs/roadmap/REQ-*-roadmap.yaml`。
3. 创建第一个 sprint：`docs/sprints/SPRINT-*.yaml`。
4. 生成 PRD、RFC、ticket 和 test plan。
5. 在 `docs/reviews/FLOW-*.md` 写入流程证据报告。
6. 返回生成路径前运行 schema 校验。

## 控制平面职责

- 让项目工作流产物可发现。
- 让质量门禁显式化。
- 让成熟度可见。
- 让进化提案绑定证据。
- 避免交易、账户风险和 skill 晋升逻辑失控。
