from __future__ import annotations

import html
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from .models import Gate, Requirement, Roadmap, SprintPlan, Ticket
from .storage import load_model


class GateEvidence(BaseModel):
    gate: str
    passed: bool
    detail: str


class WorkItem(BaseModel):
    id: str
    requirement_id: str
    title: str
    kind: str
    status: str
    risk_level: str = "medium"
    milestone: str | None = None
    gates: list[GateEvidence] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)


class RequirementProgress(BaseModel):
    id: str
    title: str
    status: str
    total_tickets: int
    completed_tickets: int
    in_progress_tickets: int
    blocked_tickets: int


class CommitRecord(BaseModel):
    short_sha: str
    sha: str
    author: str
    committed_at: str
    subject: str
    url: str | None = None


class DashboardModel(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: dict[str, int]
    requirements: list[RequirementProgress]
    work_items: list[WorkItem]
    commits: list[CommitRecord] = Field(default_factory=list)


def collect_dashboard(root: Path) -> DashboardModel:
    requirements = _load_requirements(root)
    roadmaps = _load_roadmaps(root)
    sprint_ticket_ids = _load_sprint_ticket_ids(root)

    work_items: list[WorkItem] = []
    progress: list[RequirementProgress] = []

    for requirement in requirements:
        roadmap = roadmaps.get(requirement.id)
        requirement_status = "已拆解" if roadmap else "待拆解"
        tickets = roadmap.tickets if roadmap else []

        work_items.append(
            WorkItem(
                id=requirement.id,
                requirement_id=requirement.id,
                title=requirement.title,
                kind="需求",
                status=requirement_status,
                risk_level="medium",
                deliverables=[f"docs/requirements/{requirement.id}.yaml"],
            )
        )

        ticket_items = [
            _ticket_to_work_item(root, requirement.id, ticket, sprint_ticket_ids) for ticket in tickets
        ]
        work_items.extend(ticket_items)

        progress.append(
            RequirementProgress(
                id=requirement.id,
                title=requirement.title,
                status=requirement_status,
                total_tickets=len(ticket_items),
                completed_tickets=sum(item.status == "测试完成" for item in ticket_items),
                in_progress_tickets=sum(item.status == "开发中" for item in ticket_items),
                blocked_tickets=sum(item.status == "门禁受阻" for item in ticket_items),
            )
        )

    summary = {
        "需求总数": len(requirements),
        "任务总数": sum(1 for item in work_items if item.kind == "任务"),
        "待拆解": sum(item.status == "待拆解" for item in work_items),
        "待开发": sum(item.status == "待开发" for item in work_items),
        "开发中": sum(item.status == "开发中" for item in work_items),
        "测试完成": sum(item.status == "测试完成" for item in work_items),
        "门禁受阻": sum(item.status == "门禁受阻" for item in work_items),
    }
    return DashboardModel(
        summary=summary,
        requirements=progress,
        work_items=work_items,
        commits=_load_recent_commits(root),
    )


def write_dashboard(root: Path) -> tuple[Path, Path]:
    dashboard = collect_dashboard(root)
    target = root / "docs" / "dashboard"
    target.mkdir(parents=True, exist_ok=True)

    json_path = target / "status.json"
    html_path = target / "index.html"
    json_path.write_text(
        json.dumps(dashboard.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    html_path.write_text(render_dashboard_html(dashboard), encoding="utf-8")
    return json_path, html_path


def render_dashboard_html(dashboard: DashboardModel) -> str:
    columns = ["待拆解", "待开发", "开发中", "测试完成", "门禁受阻"]
    cards_by_status = {
        status: [item for item in dashboard.work_items if item.status == status] for status in columns
    }
    summary_cards = "\n".join(
        f'<div class="metric"><span>{html.escape(name)}</span><strong>{value}</strong></div>'
        for name, value in dashboard.summary.items()
    )
    requirement_rows = "\n".join(_render_requirement_row(item) for item in dashboard.requirements)
    commit_rows = "\n".join(_render_commit_row(item) for item in dashboard.commits)
    board_columns = "\n".join(
        f"""
        <section class="column">
          <h2>{status}<span>{len(cards_by_status[status])}</span></h2>
          {''.join(_render_work_item_card(item) for item in cards_by_status[status])}
        </section>
        """
        for status in columns
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>投资 Agent Harness 面板</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
      background: #f6f7f9;
      color: #20242a;
    }}
    body {{ margin: 0; }}
    header {{
      padding: 24px 32px 16px;
      border-bottom: 1px solid #d8dde6;
      background: #ffffff;
    }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    .time {{ color: #667085; font-size: 14px; }}
    main {{ padding: 24px 32px 40px; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .metric {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
      padding: 14px;
    }}
    .metric span {{ display: block; color: #667085; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 26px; }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(280px, 360px) 1fr;
      gap: 20px;
      align-items: start;
    }}
    .panel {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
      padding: 16px;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 9px 6px; border-bottom: 1px solid #edf0f5; text-align: left; }}
    th {{ color: #667085; font-weight: 600; }}
    .board {{
      display: grid;
      grid-template-columns: repeat(5, minmax(190px, 1fr));
      gap: 12px;
      overflow-x: auto;
    }}
    .column {{
      min-height: 360px;
      background: #eef1f5;
      border-radius: 8px;
      padding: 10px;
    }}
    .column h2 {{
      margin: 2px 4px 10px;
      font-size: 15px;
      display: flex;
      justify-content: space-between;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 10px;
    }}
    .card h3 {{ margin: 0 0 8px; font-size: 14px; line-height: 1.35; }}
    .meta {{ color: #667085; font-size: 12px; margin-bottom: 8px; }}
    .gates {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .gate {{
      font-size: 11px;
      padding: 3px 6px;
      border-radius: 999px;
      background: #f0f7ee;
      color: #2d6a35;
    }}
    .gate.fail {{ background: #fff2e8; color: #9a3412; }}
    .commit-list {{ margin-top: 16px; }}
    .commit-row {{ padding: 10px 0; border-bottom: 1px solid #edf0f5; }}
    .commit-row a {{ color: #175cd3; font-weight: 600; text-decoration: none; }}
    .commit-row div {{ margin-top: 4px; color: #475467; font-size: 12px; }}
    @media (max-width: 980px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .board {{ grid-template-columns: repeat(5, 220px); }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>投资 Agent Harness 面板</h1>
    <div class="time">生成时间：{dashboard.generated_at.isoformat()}</div>
  </header>
  <main>
    <section class="metrics">{summary_cards}</section>
    <section class="layout">
      <aside class="panel">
        <h2>需求进度</h2>
        <table>
          <thead><tr><th>需求</th><th>完成</th><th>开发中</th><th>受阻</th></tr></thead>
          <tbody>{requirement_rows}</tbody>
        </table>
        <section class="commit-list">
          <h2>最近 GitHub 提交</h2>
          {commit_rows}
        </section>
      </aside>
      <section class="board">{board_columns}</section>
    </section>
  </main>
</body>
</html>
"""


def _load_requirements(root: Path) -> list[Requirement]:
    paths = sorted((root / "docs" / "requirements").glob("REQ-*.yaml"))
    return [load_model(path, Requirement) for path in paths]


def _load_roadmaps(root: Path) -> dict[str, Roadmap]:
    roadmaps: dict[str, Roadmap] = {}
    for path in sorted((root / "docs" / "roadmap").glob("*-roadmap.yaml")):
        roadmap = load_model(path, Roadmap)
        roadmaps[roadmap.requirement_id] = roadmap
    return roadmaps


def _load_sprint_ticket_ids(root: Path) -> set[str]:
    ticket_ids: set[str] = set()
    for path in sorted((root / "docs" / "sprints").glob("SPRINT-*.yaml")):
        data = load_model(path, SprintPlan)
        ticket_ids.update(data.tickets)
    return ticket_ids


def _load_recent_commits(root: Path, limit: int = 8) -> list[CommitRecord]:
    try:
        output = subprocess.check_output(
            [
                "git",
                "log",
                f"--max-count={limit}",
                "--date=iso-strict",
                "--pretty=format:%h%x1f%H%x1f%an%x1f%ad%x1f%s",
            ],
            cwd=root,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    base_url = _github_commit_base_url(root)
    commits: list[CommitRecord] = []
    for line in output.splitlines():
        parts = line.split("\x1f")
        if len(parts) != 5:
            continue
        short_sha, sha, author, committed_at, subject = parts
        commits.append(
            CommitRecord(
                short_sha=short_sha,
                sha=sha,
                author=author,
                committed_at=committed_at,
                subject=subject,
                url=f"{base_url}/{sha}" if base_url else None,
            )
        )
    return commits


def _github_commit_base_url(root: Path) -> str | None:
    try:
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=root,
            text=True,
            encoding="utf-8",
            errors="replace",
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    if remote.startswith("git@github.com:"):
        repo = remote.removeprefix("git@github.com:").removesuffix(".git")
        return f"https://github.com/{repo}/commit"
    if remote.startswith("https://github.com/"):
        repo = remote.removeprefix("https://github.com/").removesuffix(".git")
        return f"https://github.com/{repo}/commit"
    return None


def _ticket_to_work_item(
    root: Path, requirement_id: str, ticket: Ticket, sprint_ticket_ids: set[str]
) -> WorkItem:
    gates = [_gate_evidence(root, requirement_id, gate) for gate in ticket.gates]
    if gates and all(gate.passed for gate in gates):
        status = "测试完成"
    elif ticket.id in sprint_ticket_ids and any(not gate.passed for gate in gates):
        status = "开发中"
    elif any(not gate.passed for gate in gates if gate.gate in {"backtest", "shadow_live", "human_approval"}):
        status = "门禁受阻"
    else:
        status = "待开发"

    return WorkItem(
        id=f"{requirement_id}:{ticket.id}",
        requirement_id=requirement_id,
        title=ticket.title,
        kind="任务",
        status=status,
        risk_level=ticket.risk_level.value,
        milestone=ticket.milestone,
        gates=gates,
        deliverables=ticket.deliverables,
    )


def _gate_evidence(root: Path, requirement_id: str, gate: Gate) -> GateEvidence:
    evidence = {
        Gate.requirement_review: (root / "docs" / "requirements" / f"{requirement_id}.yaml").exists(),
        Gate.prototype_review: any((root / "docs" / "prototypes").glob("*.md")),
        Gate.design_review: any((root / "docs" / "rfc").glob("*.md"))
        or any((root / "docs" / "adr").glob("*.md")),
        Gate.unit_tests: any((root / "tests").glob("test_*.py")),
        Gate.integration_tests: any((root / "tests").glob("test_*.py")),
        Gate.data_quality: any((root / "docs" / "evals").glob("*.yaml")),
        Gate.backtest: any((root / "docs" / "evals").glob("*SKILL*.yaml")),
        Gate.shadow_live: any((root / "docs" / "reviews").glob("*shadow*.md")),
        Gate.human_approval: any((root / "docs" / "releases").glob("*.md")),
        Gate.rollback_plan: any((root / "docs" / "releases").glob("*.md")),
    }
    details = {
        Gate.requirement_review: f"docs/requirements/{requirement_id}.yaml",
        Gate.prototype_review: "docs/prototypes/*.md",
        Gate.design_review: "docs/rfc 或 docs/adr",
        Gate.unit_tests: "tests/test_*.py",
        Gate.integration_tests: "tests/test_*.py",
        Gate.data_quality: "docs/evals/*.yaml",
        Gate.backtest: "docs/evals/*SKILL*.yaml",
        Gate.shadow_live: "docs/reviews/*shadow*.md",
        Gate.human_approval: "docs/releases/*.md",
        Gate.rollback_plan: "docs/releases/*.md",
    }
    return GateEvidence(gate=gate.value, passed=evidence[gate], detail=details[gate])


def _render_requirement_row(requirement: RequirementProgress) -> str:
    return (
        "<tr>"
        f"<td>{html.escape(requirement.id)}<br>{html.escape(requirement.title)}</td>"
        f"<td>{requirement.completed_tickets}/{requirement.total_tickets}</td>"
        f"<td>{requirement.in_progress_tickets}</td>"
        f"<td>{requirement.blocked_tickets}</td>"
        "</tr>"
    )


def _render_work_item_card(item: WorkItem) -> str:
    gate_html = "".join(
        f'<span class="gate{" fail" if not gate.passed else ""}">{html.escape(gate.gate)}</span>'
        for gate in item.gates
    )
    return f"""
    <article class="card">
      <h3>{html.escape(item.title)}</h3>
      <div class="meta">{html.escape(item.id)} · {html.escape(item.kind)} · 风险 {html.escape(item.risk_level)}</div>
      <div class="gates">{gate_html}</div>
    </article>
    """


def _render_commit_row(commit: CommitRecord) -> str:
    subject = html.escape(commit.subject)
    short_sha = html.escape(commit.short_sha)
    if commit.url:
        sha_html = f'<a href="{html.escape(commit.url)}">{short_sha}</a>'
    else:
        sha_html = f"<strong>{short_sha}</strong>"
    return f"""
    <article class="commit-row">
      {sha_html} {subject}
      <div>{html.escape(commit.author)} · {html.escape(commit.committed_at)}</div>
    </article>
    """
