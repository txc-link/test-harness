from pathlib import Path

from harness_engine.artifacts import scaffold_from_template
from harness_engine.status import collect_status, status_markdown


ROOT = Path(__file__).resolve().parents[1]


def test_scaffold_from_template_creates_named_artifact(tmp_path: Path) -> None:
    (tmp_path / "templates").mkdir()
    (tmp_path / "docs" / "rfc").mkdir(parents=True)
    (tmp_path / "templates" / "rfc.md").write_text("# RFC: <Title>\n", encoding="utf-8")

    path = scaffold_from_template(tmp_path, "rfc", "Harness Control Plane")

    assert path.name == "RFC-harness-control-plane.md"
    assert path.read_text(encoding="utf-8") == "# RFC: Harness Control Plane\n"


def test_collect_status_reports_maturity_level() -> None:
    status = collect_status(ROOT)

    assert status.maturity_level >= 1
    assert any(check.name == "ci:github-actions" and check.passed for check in status.checks)


def test_status_markdown_contains_pass_fail_table() -> None:
    status = collect_status(ROOT)
    markdown = status_markdown(status)

    assert "| Check | Result | Detail |" in markdown
    assert "Maturity level" in markdown

