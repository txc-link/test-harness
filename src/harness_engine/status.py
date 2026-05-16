from __future__ import annotations

from pathlib import Path

from .artifacts import REQUIRED_DIRECTORIES, REQUIRED_DOCS, REQUIRED_TEMPLATES
from .models import HarnessCheck, HarnessStatus


def _exists_check(root: Path, name: str, relative_path: str) -> HarnessCheck:
    path = root / relative_path
    return HarnessCheck(
        name=name,
        passed=path.exists(),
        detail=relative_path if path.exists() else f"Missing {relative_path}",
    )


def collect_status(root: Path) -> HarnessStatus:
    checks: list[HarnessCheck] = []

    for folder in REQUIRED_DIRECTORIES:
        checks.append(_exists_check(root, f"directory:{folder}", folder))
    for doc in REQUIRED_DOCS:
        checks.append(_exists_check(root, f"doc:{doc}", doc))
    for template in REQUIRED_TEMPLATES:
        checks.append(_exists_check(root, f"template:{template}", template))

    checks.extend(
        [
            _exists_check(root, "ci:github-actions", ".github/workflows/ci.yml"),
            _exists_check(root, "collab:pr-template", ".github/pull_request_template.md"),
            _exists_check(root, "local-check:script", "scripts/check.ps1"),
            _exists_check(root, "codex:ecc-config", ".codex/config.toml"),
        ]
    )

    maturity_level = _maturity_level(checks)
    return HarnessStatus(maturity_level=maturity_level, checks=checks)


def _maturity_level(checks: list[HarnessCheck]) -> int:
    passed_names = {check.name for check in checks if check.passed}
    if not all(check.passed for check in checks):
        return 1
    if {
        "doc:docs/QUALITY_GATES.md",
        "doc:docs/DELIVERY_PIPELINE.md",
        "doc:docs/RISK_CONTROL.md",
        "ci:github-actions",
    }.issubset(passed_names):
        return 2
    return 1


def status_markdown(status: HarnessStatus) -> str:
    lines = [
        "# Harness Status",
        "",
        f"- Generated at: {status.generated_at.isoformat()}",
        f"- Maturity level: {status.maturity_level}",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for check in status.checks:
        result = "PASS" if check.passed else "FAIL"
        lines.append(f"| {check.name} | {result} | {check.detail} |")
    return "\n".join(lines) + "\n"
