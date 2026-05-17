from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_github_actions_generates_dashboard_artifact() -> None:
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text())
    steps = workflow["jobs"]["test"]["steps"]
    rendered_steps = "\n".join(str(step) for step in steps)

    assert "python -m harness_engine.cli dashboard" in rendered_steps
    assert "actions/upload-artifact" in rendered_steps
    assert "docs/dashboard/index.html" in rendered_steps
    assert "docs/dashboard/status.json" in rendered_steps


def test_spec_cicd_files_follow_plan_run_sync_layout() -> None:
    spec_root = ROOT / ".moai" / "specs" / "SPEC-CI-0001"

    for name in ["spec.md", "plan.md", "scenarios.md", "risks.md", "progress.md"]:
        assert (spec_root / name).exists()

    spec = (spec_root / "spec.md").read_text(encoding="utf-8")
    assert "REQ-CI-001" in spec
    assert "AC-CI-001" in spec
