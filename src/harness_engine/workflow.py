from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .artifacts import REQUIRED_DIRECTORIES, scaffold_from_template, slugify
from .models import Requirement, Roadmap, SprintPlan
from .planner import default_evaluations, requirement_from_text, roadmap_from_requirement, sprint_from_roadmap
from .storage import dump_model, next_id


@dataclass(frozen=True)
class DevelopmentFlowResult:
    requirement: Path
    roadmap: Path
    sprint: Path
    prd: Path
    rfc: Path
    ticket: Path
    test_plan: Path
    report: Path

    def paths(self) -> list[Path]:
        return [
            self.requirement,
            self.roadmap,
            self.sprint,
            self.prd,
            self.rfc,
            self.ticket,
            self.test_plan,
            self.report,
        ]


def ensure_baseline(root: Path) -> None:
    for folder in REQUIRED_DIRECTORIES:
        (root / folder).mkdir(parents=True, exist_ok=True)

    for spec in default_evaluations():
        path = root / "docs" / "evals" / f"{spec.id}.yaml"
        if not path.exists():
            dump_model(path, spec)


def run_development_flow(root: Path, text: str, title: str | None = None) -> DevelopmentFlowResult:
    """Create a small, auditable requirement-to-test development flow."""
    ensure_baseline(root)

    req_id = next_id(root / "docs" / "requirements", "REQ")
    requirement = requirement_from_text(req_id, text)
    if title:
        requirement.title = title

    requirement_path = root / "docs" / "requirements" / f"{requirement.id}.yaml"
    dump_model(requirement_path, requirement)

    roadmap = roadmap_from_requirement(requirement)
    roadmap_path = root / "docs" / "roadmap" / f"{requirement.id}-roadmap.yaml"
    dump_model(roadmap_path, roadmap)

    sprint = sprint_from_roadmap(roadmap)
    sprint.id = f"SPRINT-{requirement.id.removeprefix('REQ-')}"
    sprint_path = root / "docs" / "sprints" / f"{sprint.id}.yaml"
    dump_model(sprint_path, sprint)

    artifact_title = title or requirement.title
    prd_path = scaffold_from_template(root, "prd", artifact_title)
    rfc_path = scaffold_from_template(root, "rfc", artifact_title)
    ticket_path = scaffold_from_template(root, "ticket", artifact_title)
    test_plan_path = scaffold_from_template(root, "test-plan", artifact_title)

    report_path = root / "docs" / "reviews" / f"FLOW-{requirement.id}-{slugify(artifact_title)}.md"
    artifact_paths = [
        requirement_path,
        roadmap_path,
        sprint_path,
        prd_path,
        rfc_path,
        ticket_path,
        test_plan_path,
    ]
    report_path.write_text(
        flow_report(root, requirement, roadmap, sprint, artifact_title, artifact_paths),
        encoding="utf-8",
    )

    return DevelopmentFlowResult(
        requirement=requirement_path,
        roadmap=roadmap_path,
        sprint=sprint_path,
        prd=prd_path,
        rfc=rfc_path,
        ticket=ticket_path,
        test_plan=test_plan_path,
        report=report_path,
    )


def flow_report(
    root: Path,
    requirement: Requirement,
    roadmap: Roadmap,
    sprint: SprintPlan,
    title: str,
    artifact_paths: list[Path],
) -> str:
    ticket_rows = "\n".join(
        f"| {ticket.id} | {ticket.title} | {ticket.risk_level.value} | "
        f"{', '.join(gate.value for gate in ticket.gates)} |"
        for ticket in roadmap.tickets
    )
    artifact_lines = "\n".join(
        f"- `{path.relative_to(root).as_posix()}`" for path in artifact_paths
    )

    return f"""# Development Flow Report: {title}

## Requirement

- ID: {requirement.id}
- Title: {requirement.title}

## Decomposition

- Roadmap milestones: {len(roadmap.milestones)}
- Sprint: {sprint.id}
- Sprint tickets: {", ".join(sprint.tickets)}

## Generated Delivery Artifacts

{artifact_lines}

## Ticket Gates

| Ticket | Title | Risk | Gates |
| --- | --- | --- | --- |
{ticket_rows}

## Verification Command

```powershell
.\\scripts\\check.ps1
```

## Exit Criteria

{chr(10).join(f"- {criterion}" for criterion in sprint.exit_criteria)}
"""
