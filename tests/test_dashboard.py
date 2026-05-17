from __future__ import annotations

import shutil
from pathlib import Path

from harness_engine.dashboard import collect_dashboard, render_dashboard_html, write_dashboard

ROOT = Path(__file__).resolve().parents[1]


def test_collect_dashboard_reports_requirements_and_work_items() -> None:
    dashboard = collect_dashboard(ROOT)

    assert dashboard.summary["需求总数"] >= 1
    assert dashboard.summary["任务总数"] >= 1
    assert any(item.kind == "任务" for item in dashboard.work_items)
    assert any(item.status == "开发中" for item in dashboard.work_items)
    assert any(item.status == "测试完成" for item in dashboard.work_items)


def test_render_dashboard_html_contains_core_board_sections() -> None:
    html = render_dashboard_html(collect_dashboard(ROOT))

    assert "投资 Agent Harness 面板" in html
    assert "需求进度" in html
    assert "开发中" in html
    assert "测试完成" in html


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

    json_path, html_path = write_dashboard(tmp_path)

    assert json_path.exists()
    assert html_path.exists()
    assert "status.json" == json_path.name
    assert "index.html" == html_path.name
