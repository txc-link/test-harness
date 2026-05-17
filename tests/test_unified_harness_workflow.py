from __future__ import annotations

from pathlib import Path

from harness_engine.artifacts import scaffold_from_template

ROOT = Path(__file__).resolve().parents[1]


def test_unified_workflow_documents_trellis_finish_loop() -> None:
    doc = (ROOT / "docs" / "UNIFIED_HARNESS_WORKFLOW.md").read_text(encoding="utf-8")

    assert "Trellis" in doc
    assert "Plan" in doc
    assert "Implement" in doc
    assert "Verify" in doc
    assert "Finish" in doc
    assert ".trellis/spec/" in doc


def test_trellis_task_template_can_be_scaffolded(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "trellis_task.md").write_text("# <Title>\n## Finish\n", encoding="utf-8")

    path = scaffold_from_template(tmp_path, "trellis-task", "盯盘告警控制台")

    assert path.exists()
    assert path.parent.name == "tasks"
    assert "盯盘告警控制台" in path.read_text(encoding="utf-8")
