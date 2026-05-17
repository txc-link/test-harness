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


class TrellisArtifact(BaseModel):
    kind: str
    phase: str
    title: str
    path: str


class TaskTreeGate(BaseModel):
    name: str
    passed: bool
    detail: str


class TaskTreeTicketNode(BaseModel):
    id: str
    title: str
    status: str
    risk_level: str
    milestone: str | None = None
    gates: list[TaskTreeGate] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)


class TaskTreeRequirementNode(BaseModel):
    id: str
    title: str
    status: str
    source_path: str
    total_tickets: int
    completed_tickets: int
    tickets: list[TaskTreeTicketNode] = Field(default_factory=list)


class DashboardModel(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: dict[str, int]
    requirements: list[RequirementProgress]
    work_items: list[WorkItem]
    commits: list[CommitRecord] = Field(default_factory=list)
    trellis_artifacts: list[TrellisArtifact] = Field(default_factory=list)
    trellis_summary: dict[str, int] = Field(default_factory=dict)
    task_tree: list[TaskTreeRequirementNode] = Field(default_factory=list)


def collect_dashboard(root: Path) -> DashboardModel:
    requirements = _load_requirements(root)
    roadmaps = _load_roadmaps(root)
    sprint_ticket_ids = _load_sprint_ticket_ids(root)
    trellis_artifacts = _load_trellis_artifacts(root)

    work_items: list[WorkItem] = []
    progress: list[RequirementProgress] = []
    task_tree: list[TaskTreeRequirementNode] = []

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
        task_tree.append(
            _build_task_tree_requirement(
                requirement=requirement,
                status=requirement_status,
                ticket_items=ticket_items,
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
        trellis_artifacts=trellis_artifacts,
        trellis_summary=_summarize_trellis(trellis_artifacts),
        task_tree=task_tree,
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
    trellis_lanes = "\n".join(
        _render_trellis_lane(kind, dashboard.trellis_artifacts)
        for kind in ["共享规格", "任务中心", "工作区", "工作日志"]
    )
    task_tree_html = "\n".join(_render_task_tree_requirement(node) for node in dashboard.task_tree)

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
    h2 {{ margin-top: 0; font-size: 18px; }}
    .time {{ color: #667085; font-size: 14px; }}
    main {{ padding: 24px 32px 40px; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .metric, .panel, .trellis-shell {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
    }}
    .metric {{ padding: 14px; }}
    .metric span {{ display: block; color: #667085; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 26px; }}
    .trellis-shell {{ padding: 18px; margin-bottom: 20px; }}
    .section-title {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 14px;
    }}
    .section-title p {{ margin: 0; color: #667085; font-size: 13px; }}
    .phase-flow {{
      display: grid;
      grid-template-columns: repeat(4, minmax(150px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    .phase-step {{
      border: 1px solid #d8dde6;
      border-left: 4px solid #2563eb;
      border-radius: 8px;
      padding: 12px;
      background: #f8fafc;
    }}
    .phase-step strong {{ display: block; margin-bottom: 5px; }}
    .phase-step span {{ color: #475467; font-size: 12px; line-height: 1.5; }}
    .trellis-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(180px, 1fr));
      gap: 12px;
    }}
    .trellis-lane {{
      background: #f6f7f9;
      border: 1px solid #e4e7ec;
      border-radius: 8px;
      padding: 12px;
      min-height: 150px;
    }}
    .trellis-lane h3 {{
      margin: 0 0 10px;
      font-size: 14px;
      display: flex;
      justify-content: space-between;
    }}
    .trellis-item {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
      padding: 10px;
      margin-bottom: 8px;
    }}
    .trellis-item strong {{ display: block; font-size: 13px; line-height: 1.35; }}
    .trellis-item span {{ display: block; margin-top: 6px; color: #667085; font-size: 11px; }}
    .task-tree-shell {{
      background: #ffffff;
      border: 1px solid #d8dde6;
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 20px;
    }}
    .task-tree {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 12px;
    }}
    .tree-node {{
      border: 1px solid #d8dde6;
      border-radius: 8px;
      background: #f8fafc;
      padding: 12px;
    }}
    .tree-node summary {{
      cursor: pointer;
      font-weight: 700;
      line-height: 1.4;
    }}
    .tree-node summary span {{
      color: #667085;
      font-size: 12px;
      font-weight: 500;
      margin-left: 6px;
    }}
    .tree-children {{
      margin-top: 10px;
      padding-left: 12px;
      border-left: 2px solid #d8dde6;
    }}
    .ticket-node {{
      background: #ffffff;
      border: 1px solid #e4e7ec;
      border-radius: 8px;
      padding: 10px;
      margin-bottom: 10px;
    }}
    .ticket-node summary {{ font-size: 13px; font-weight: 700; }}
    .deliverables {{
      margin: 8px 0 0;
      padding-left: 18px;
      color: #475467;
      font-size: 12px;
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(280px, 360px) 1fr;
      gap: 20px;
      align-items: start;
    }}
    .panel {{ padding: 16px; }}
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
    @media (max-width: 1180px) {{
      .trellis-grid, .phase-flow {{ grid-template-columns: repeat(2, minmax(180px, 1fr)); }}
    }}
    @media (max-width: 980px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .board {{ grid-template-columns: repeat(5, 220px); }}
    }}
    @media (max-width: 620px) {{
      main, header {{ padding-left: 18px; padding-right: 18px; }}
      .trellis-grid, .phase-flow {{ grid-template-columns: 1fr; }}
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
    <section class="trellis-shell">
      <div class="section-title">
        <h2>Trellis 控制台</h2>
        <p>从共享规格到任务、工作区、日志回写，展示 Harness 的完整执行轨迹。</p>
      </div>
      <div class="phase-flow">
        {_render_phase_step("Plan", "需求澄清、规格沉淀、任务拆解和排期。")}
        {_render_phase_step("Implement", "在任务中心领取工作，生成代码、文档和原型。")}
        {_render_phase_step("Verify", "在隔离工作区运行测试、门禁和 CI/CD 验证。")}
        {_render_phase_step("Finish", "记录复盘结论，把有效反馈回写到规格和技能。")}
      </div>
      <div class="trellis-grid">{trellis_lanes}</div>
    </section>
    <section class="task-tree-shell">
      <div class="section-title">
        <h2>任务树视图</h2>
        <p>按 Trellis 的任务拆解方式展示需求、任务、门禁和交付物的父子关系。</p>
      </div>
      <div class="task-tree">{task_tree_html}</div>
    </section>
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


def _load_trellis_artifacts(root: Path) -> list[TrellisArtifact]:
    folders = {
        "共享规格": ("spec", "Plan"),
        "任务中心": ("tasks", "Implement"),
        "工作区": ("workspaces", "Verify"),
        "工作日志": ("journal", "Finish"),
    }
    artifacts: list[TrellisArtifact] = []
    trellis_root = root / ".trellis"
    for kind, (folder, phase) in folders.items():
        for path in sorted((trellis_root / folder).glob("*.md")):
            artifacts.append(
                TrellisArtifact(
                    kind=kind,
                    phase=phase,
                    title=_read_markdown_title(path),
                    path=_relative_path(root, path),
                )
            )
    return artifacts


def _summarize_trellis(artifacts: list[TrellisArtifact]) -> dict[str, int]:
    return {
        kind: sum(artifact.kind == kind for artifact in artifacts)
        for kind in ["共享规格", "任务中心", "工作区", "工作日志"]
    }


def _build_task_tree_requirement(
    requirement: Requirement, status: str, ticket_items: list[WorkItem]
) -> TaskTreeRequirementNode:
    tickets = [
        TaskTreeTicketNode(
            id=item.id,
            title=item.title,
            status=item.status,
            risk_level=item.risk_level,
            milestone=item.milestone,
            gates=[
                TaskTreeGate(name=gate.gate, passed=gate.passed, detail=gate.detail)
                for gate in item.gates
            ],
            deliverables=item.deliverables,
        )
        for item in ticket_items
    ]
    return TaskTreeRequirementNode(
        id=requirement.id,
        title=requirement.title,
        status=status,
        source_path=f"docs/requirements/{requirement.id}.yaml",
        total_tickets=len(tickets),
        completed_tickets=sum(ticket.status == "测试完成" for ticket in tickets),
        tickets=tickets,
    )


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


def _read_markdown_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped.removeprefix("# ").strip()
    except OSError:
        return path.stem
    return path.stem


def _relative_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


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


def _render_trellis_lane(kind: str, artifacts: list[TrellisArtifact]) -> str:
    lane_artifacts = [artifact for artifact in artifacts if artifact.kind == kind]
    items = "".join(_render_trellis_item(artifact) for artifact in lane_artifacts)
    if not items:
        items = '<div class="trellis-item"><strong>暂无工件</strong><span>等待 Harness 生成</span></div>'
    return f"""
    <section class="trellis-lane">
      <h3>{html.escape(kind)}<span>{len(lane_artifacts)}</span></h3>
      {items}
    </section>
    """


def _render_trellis_item(artifact: TrellisArtifact) -> str:
    return f"""
    <article class="trellis-item">
      <strong>{html.escape(artifact.title)}</strong>
      <span>{html.escape(artifact.phase)} · {html.escape(artifact.path)}</span>
    </article>
    """


def _render_task_tree_requirement(node: TaskTreeRequirementNode) -> str:
    tickets = "".join(_render_task_tree_ticket(ticket) for ticket in node.tickets)
    if not tickets:
        tickets = '<div class="ticket-node">等待拆解任务</div>'
    return f"""
    <details class="tree-node" open>
      <summary>
        {html.escape(node.id)} · {html.escape(node.title)}
        <span>{html.escape(node.status)} · {node.completed_tickets}/{node.total_tickets}</span>
      </summary>
      <div class="meta">{html.escape(node.source_path)}</div>
      <div class="tree-children">{tickets}</div>
    </details>
    """


def _render_task_tree_ticket(ticket: TaskTreeTicketNode) -> str:
    gates = "".join(
        f'<span class="gate{" fail" if not gate.passed else ""}" title="{html.escape(gate.detail)}">'
        f"{html.escape(gate.name)}</span>"
        for gate in ticket.gates
    )
    deliverables = "".join(
        f"<li>{html.escape(deliverable)}</li>" for deliverable in ticket.deliverables
    )
    if deliverables:
        deliverables = f'<ul class="deliverables">{deliverables}</ul>'
    return f"""
    <details class="ticket-node">
      <summary>
        {html.escape(ticket.title)}
        <span>{html.escape(ticket.status)} · 风险 {html.escape(ticket.risk_level)}</span>
      </summary>
      <div class="meta">{html.escape(ticket.id)} · {html.escape(ticket.milestone or "未分配里程碑")}</div>
      <div class="gates">{gates}</div>
      {deliverables}
    </details>
    """


def _render_phase_step(name: str, description: str) -> str:
    return f"""
    <article class="phase-step">
      <strong>{html.escape(name)}</strong>
      <span>{html.escape(description)}</span>
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
