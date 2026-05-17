from __future__ import annotations

import shutil
from pathlib import Path

from harness_engine.dashboard import collect_dashboard, render_dashboard_html, write_dashboard

ROOT = Path(__file__).resolve().parents[1]


def test_collect_dashboard_reports_requirements_and_work_items() -> None:
    dashboard = collect_dashboard(ROOT)

    assert dashboard.summary["需求总数"] >= 1
    assert dashboard.summary["任务总数"] >= 1
    assert dashboard.commits
    assert dashboard.commits[0].url is None or dashboard.commits[0].url.startswith(
        "https://github.com/"
    )
    assert dashboard.trellis_summary["共享规格"] >= 1
    assert dashboard.trellis_summary["任务中心"] >= 1
    assert any(artifact.phase == "Plan" for artifact in dashboard.trellis_artifacts)
    assert dashboard.task_tree
    assert any(node.tickets for node in dashboard.task_tree)
    assert any(ticket.gates for node in dashboard.task_tree for ticket in node.tickets)
    assert dashboard.code_traces
    assert any(trace.commits for trace in dashboard.code_traces)
    assert all(trace.branch for trace in dashboard.code_traces)
    assert any(item.kind == "任务" for item in dashboard.work_items)
    assert any(item.status == "开发中" for item in dashboard.work_items)
    assert any(item.status == "测试完成" for item in dashboard.work_items)


def test_render_dashboard_html_contains_core_board_sections() -> None:
    page_html = render_dashboard_html(collect_dashboard(ROOT))

    assert "投资 Agent Harness 面板" in page_html
    assert "Trellis 控制台" in page_html
    assert "Plan" in page_html
    assert "Implement" in page_html
    assert "Verify" in page_html
    assert "Finish" in page_html
    assert ".trellis/spec" in page_html
    assert "任务树视图" in page_html
    assert "tree-node" in page_html
    assert "ticket-node" in page_html
    assert "任务到代码追踪链" in page_html
    assert "trace-card" in page_html
    assert "GitHub Actions" in page_html
    assert "需求进度" in page_html
    assert "最近 GitHub 提交" in page_html
    assert "开发中" in page_html
    assert "测试完成" in page_html


def test_write_dashboard_creates_json_and_html(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    for name in ["requirements", "roadmap", "sprints", "evals", "reviews", "releases"]:
        source = ROOT / "docs" / name
        if source.exists():
            shutil.copytree(source, docs / name)
        else:
            (docs / name).mkdir()
    shutil.copytree(ROOT / "tests", tmp_path / "tests")
    shutil.copytree(ROOT / ".trellis", tmp_path / ".trellis")

    json_path, html_path = write_dashboard(tmp_path)

    assert json_path.exists()
    assert html_path.exists()
    assert "status.json" == json_path.name
    assert "index.html" == html_path.name
