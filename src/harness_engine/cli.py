from __future__ import annotations

from pathlib import Path

import typer

from .artifacts import scaffold_from_template
from .dashboard import write_dashboard
from .models import Requirement, Roadmap
from .planner import requirement_from_text, roadmap_from_requirement, sprint_from_roadmap
from .storage import dump_model, load_model, next_id
from .status import collect_status, status_markdown
from .workflow import ensure_baseline, run_development_flow

app = typer.Typer(help="Engineering harness for the self-evolving investment agent.")

ROOT = Path.cwd()


@app.command()
def init() -> None:
    """Create the standard harness directories and baseline evaluation specs."""
    ensure_baseline(ROOT)
    typer.echo("Harness initialized.")


@app.command()
def new(kind: str, title: str) -> None:
    """Scaffold a PRD, RFC, ticket, test plan, release, runbook, or evolution artifact."""
    path = scaffold_from_template(ROOT, kind, title)
    typer.echo(str(path))


@app.command()
def intake(text: str) -> None:
    """Capture a raw requirement as a structured requirement artifact."""
    req_id = next_id(ROOT / "docs" / "requirements", "REQ")
    req = requirement_from_text(req_id, text)
    path = ROOT / "docs" / "requirements" / f"{req.id}.yaml"
    dump_model(path, req)
    typer.echo(str(path))


@app.command("run")
def run_pipeline(text: str) -> None:
    """Run init, intake, plan, and validate as a single requirement pipeline."""
    init()
    req_id = next_id(ROOT / "docs" / "requirements", "REQ")
    req = requirement_from_text(req_id, text)
    req_path = ROOT / "docs" / "requirements" / f"{req.id}.yaml"
    dump_model(req_path, req)

    roadmap = roadmap_from_requirement(req)
    roadmap_path = ROOT / "docs" / "roadmap" / f"{req.id}-roadmap.yaml"
    dump_model(roadmap_path, roadmap)

    sprint = sprint_from_roadmap(roadmap)
    sprint_path = ROOT / "docs" / "sprints" / f"{sprint.id}.yaml"
    dump_model(sprint_path, sprint)

    validate()
    typer.echo("Generated:")
    typer.echo(str(req_path))
    typer.echo(str(roadmap_path))
    typer.echo(str(sprint_path))


@app.command()
def develop(text: str, title: str | None = None) -> None:
    """Run the requirement, decomposition, delivery artifact, and test-planning flow."""
    result = run_development_flow(ROOT, text, title)
    validate()
    typer.echo("Generated development flow:")
    for path in result.paths():
        typer.echo(str(path))


@app.command("develop-file")
def develop_file(requirement_file: Path, title: str | None = None) -> None:
    """Run the development flow from a UTF-8 requirement document."""
    text = requirement_file.read_text(encoding="utf-8")
    result = run_development_flow(ROOT, text, title or requirement_file.stem)
    validate()
    typer.echo("Generated development flow:")
    for path in result.paths():
        typer.echo(str(path))


@app.command()
def plan(requirement_path: Path) -> None:
    """Generate roadmap and first sprint artifacts from a requirement."""
    req = load_model(requirement_path, Requirement)
    roadmap = roadmap_from_requirement(req)
    roadmap_path = ROOT / "docs" / "roadmap" / f"{req.id}-roadmap.yaml"
    dump_model(roadmap_path, roadmap)

    sprint = sprint_from_roadmap(roadmap)
    sprint_path = ROOT / "docs" / "sprints" / f"{sprint.id}.yaml"
    dump_model(sprint_path, sprint)
    typer.echo(str(roadmap_path))
    typer.echo(str(sprint_path))


@app.command()
def validate() -> None:
    """Validate required harness artifacts and schemas."""
    required = [
        ROOT / "docs" / "evals" / "EVAL-ACCOUNT-ALPHA.yaml",
        ROOT / "docs" / "evals" / "EVAL-SKILL-EVOLUTION.yaml",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise typer.BadParameter("Missing required artifacts: " + ", ".join(str(p) for p in missing))

    for path in (ROOT / "docs" / "requirements").glob("REQ-*.yaml"):
        load_model(path, Requirement)
    for path in (ROOT / "docs" / "roadmap").glob("*-roadmap.yaml"):
        load_model(path, Roadmap)

    typer.echo("Harness validation passed.")


@app.command()
def status(write: bool = False) -> None:
    """Report harness maturity and required artifact status."""
    harness_status = collect_status(ROOT)
    markdown = status_markdown(harness_status)
    if write:
        path = ROOT / "docs" / "metrics" / "HARNESS_STATUS.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
        typer.echo(str(path))
    else:
        typer.echo(markdown)


@app.command()
def dashboard() -> None:
    """生成需求、任务、门禁和测试状态面板。"""
    json_path, html_path = write_dashboard(ROOT)
    typer.echo(str(json_path))
    typer.echo(str(html_path))


@app.command()
def maturity() -> None:
    """Print the current harness maturity level."""
    harness_status = collect_status(ROOT)
    typer.echo(f"Level {harness_status.maturity_level}")


if __name__ == "__main__":
    app()
