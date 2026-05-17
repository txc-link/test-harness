---
id: SPEC-CI-0001
title: CI/CD Harness 平台闭环
status: in-progress
owner: agent
---

# SPEC-CI-0001 CI/CD Harness 平台闭环

## 背景

投资 Agent 的工程流程需要把需求、原型、排期、开发、测试、CI、面板和发布证据串成可审计闭环。本 SPEC 用于固化 CI/CD 平台能力，避免只靠口头流程。

## EARS 需求

- REQ-CI-001：系统应当在每次 push 和 pull request 时运行 Harness 产物校验。
- REQ-CI-002：系统应当在每次 CI 运行时执行 lint 和单元测试。
- REQ-CI-003：当 CI 运行完成核心测试后，系统应当生成可视化 dashboard。
- REQ-CI-004：当 dashboard 生成后，系统应当上传 `harness-dashboard` artifact。
- REQ-CI-005：如果测试、lint 或 Harness 校验失败，系统应当阻止该提交成为发布候选。
- REQ-CI-006：当界面类需求进入开发前，系统应当要求 Figma 原型评审记录。

## 验收标准

AC-CI-001: GitHub Actions 必须执行 Harness 校验。
  - Verification: `.github/workflows/ci.yml` 包含 `python -m harness_engine.cli validate`。
  - Priority: P0

AC-CI-002: GitHub Actions 必须执行 lint 和测试。
  - Verification: `.github/workflows/ci.yml` 包含 `ruff check .` 和 `pytest`。
  - Priority: P0

AC-CI-003: GitHub Actions 必须生成 dashboard。
  - Verification: `.github/workflows/ci.yml` 包含 `python -m harness_engine.cli dashboard`。
  - Priority: P1

AC-CI-004: GitHub Actions 必须上传 dashboard artifact。
  - Verification: `.github/workflows/ci.yml` 使用 `actions/upload-artifact` 并上传 `docs/dashboard/index.html` 与 `docs/dashboard/status.json`。
  - Priority: P1

AC-CI-005: SPEC 必须保留测试场景、风险和进度文件。
  - Verification: `.moai/specs/SPEC-CI-0001/` 包含 `plan.md`、`scenarios.md`、`risks.md` 和 `progress.md`。
  - Priority: P1
