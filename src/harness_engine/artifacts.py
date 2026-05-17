from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TemplateSpec:
    kind: str
    folder: str
    template: str
    prefix: str


TEMPLATES: dict[str, TemplateSpec] = {
    "prd": TemplateSpec("prd", "docs/requirements", "templates/prd.md", "PRD"),
    "rfc": TemplateSpec("rfc", "docs/rfc", "templates/rfc.md", "RFC"),
    "ticket": TemplateSpec("ticket", "docs/sprints", "templates/ticket.md", "TICKET"),
    "test-plan": TemplateSpec("test-plan", "docs/test-plans", "templates/test_plan.md", "TEST"),
    "evolution": TemplateSpec(
        "evolution", "docs/reviews", "templates/evolution_proposal.md", "EVOLVE"
    ),
    "release": TemplateSpec("release", "docs/releases", "templates/release_checklist.md", "REL"),
    "postmortem": TemplateSpec("postmortem", "docs/incidents", "templates/postmortem.md", "POST"),
    "risk-register": TemplateSpec("risk-register", "docs/risks", "templates/risk_register.md", "RISK"),
    "runbook": TemplateSpec("runbook", "docs/runbooks", "templates/runbook.md", "RUNBOOK"),
}


REQUIRED_DIRECTORIES = [
    "docs/requirements",
    "docs/rfc",
    "docs/adr",
    "docs/roadmap",
    "docs/sprints",
    "docs/test-plans",
    "docs/evals",
    "docs/releases",
    "docs/runbooks",
    "docs/reviews",
    "docs/risks",
    "docs/incidents",
    "docs/metrics",
    "docs/dashboard",
    "data/runtime",
]


REQUIRED_DOCS = [
    "AGENTS.md",
    "README.md",
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
    "docs/SKILL_STACK.md",
    "docs/CODING_GUIDELINES.md",
    "docs/HARNESS_DASHBOARD_RESEARCH.md",
]


REQUIRED_TEMPLATES = [spec.template for spec in TEMPLATES.values()]


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {" ", "-", "_"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "untitled"


def scaffold_from_template(root: Path, kind: str, title: str) -> Path:
    if kind not in TEMPLATES:
        allowed = ", ".join(sorted(TEMPLATES))
        raise ValueError(f"Unknown artifact kind '{kind}'. Allowed: {allowed}")

    spec = TEMPLATES[kind]
    template_path = root / spec.template
    if not template_path.exists():
        raise FileNotFoundError(f"Missing template: {template_path}")

    target_folder = root / spec.folder
    target_folder.mkdir(parents=True, exist_ok=True)
    target_path = target_folder / f"{spec.prefix}-{slugify(title)}.md"

    content = template_path.read_text(encoding="utf-8").replace("<Title>", title)
    target_path.write_text(content, encoding="utf-8")
    return target_path
