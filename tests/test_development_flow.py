from pathlib import Path

from harness_engine.storage import load_model
from harness_engine.workflow import run_development_flow
from harness_engine.models import Requirement, Roadmap, SprintPlan


def write_template(root: Path, name: str) -> None:
    path = root / "templates" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# <Title>\n", encoding="utf-8")


def test_development_flow_runs_requirement_to_test_plan(tmp_path: Path) -> None:
    for template in ["prd.md", "rfc.md", "ticket.md", "test_plan.md"]:
        write_template(tmp_path, template)

    result = run_development_flow(
        tmp_path,
        "Build a harness command that turns requirements into planned, tested work.",
        "Harness Status Command",
    )

    assert all(path.exists() for path in result.paths())

    requirement = load_model(result.requirement, Requirement)
    roadmap = load_model(result.roadmap, Roadmap)
    sprint = load_model(result.sprint, SprintPlan)

    assert requirement.id == "REQ-0001"
    assert requirement.title == "Harness Status Command"
    assert roadmap.requirement_id == requirement.id
    assert sprint.id == "SPRINT-0001"
    assert sprint.tickets == ["T-0001", "T-0002"]

    report = result.report.read_text(encoding="utf-8")
    assert "Development Flow Report: Harness Status Command" in report
    assert "Verification Command" in report
    assert "T-0004" in report


def test_development_flow_preserves_utf8_requirement_text(tmp_path: Path) -> None:
    for template in ["prd.md", "rfc.md", "ticket.md", "test_plan.md"]:
        write_template(tmp_path, template)

    requirement_doc = tmp_path / "requirement.md"
    requirement_doc.write_text("从需求文档生成拆解、开发交付物和测试证据。", encoding="utf-8")

    result = run_development_flow(
        tmp_path,
        requirement_doc.read_text(encoding="utf-8"),
        "UTF8 Requirement Flow",
    )

    requirement = load_model(result.requirement, Requirement)

    assert requirement.problem == "从需求文档生成拆解、开发交付物和测试证据。"
