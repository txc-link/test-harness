from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mature_harness_docs_exist() -> None:
    required_docs = [
        "docs/HARNESS_OPERATING_MODEL.md",
        "docs/HARNESS_ENGINE.md",
        "docs/HARNESS_MATURITY_MODEL.md",
        "docs/AGENT_ROLES.md",
        "docs/QUALITY_GATES.md",
        "docs/DELIVERY_PIPELINE.md",
        "docs/RISK_CONTROL.md",
        "docs/OBSERVABILITY_METRICS.md",
        "docs/CICD.md",
        "docs/PROCESS.md",
        "docs/UNIFIED_HARNESS_WORKFLOW.md",
    ]

    missing = [path for path in required_docs if not (ROOT / path).exists()]

    assert missing == []


def test_delivery_templates_exist() -> None:
    required_templates = [
        "templates/prd.md",
        "templates/rfc.md",
        "templates/ticket.md",
        "templates/trellis_spec.md",
        "templates/trellis_task.md",
        "templates/trellis_journal.md",
        "templates/test_plan.md",
        "templates/evolution_proposal.md",
        "templates/release_checklist.md",
        "templates/postmortem.md",
        "templates/risk_register.md",
        "templates/runbook.md",
    ]

    missing = [path for path in required_templates if not (ROOT / path).exists()]

    assert missing == []


def test_trellis_context_directories_exist() -> None:
    required_dirs = [
        ".trellis/spec",
        ".trellis/tasks",
        ".trellis/workspaces",
        ".trellis/journal",
    ]

    missing = [path for path in required_dirs if not (ROOT / path).is_dir()]

    assert missing == []


def test_github_collaboration_templates_exist() -> None:
    required_files = [
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/requirement.yml",
        ".github/ISSUE_TEMPLATE/evolution.yml",
        ".github/workflows/ci.yml",
    ]

    missing = [path for path in required_files if not (ROOT / path).exists()]

    assert missing == []
