from harness_engine.planner import (
    default_evaluations,
    requirement_from_text,
    roadmap_from_requirement,
    sprint_from_roadmap,
)


def test_requirement_to_roadmap_contains_gated_evolution_ticket() -> None:
    req = requirement_from_text("REQ-0001", "Build a self-evolving investment agent.")
    roadmap = roadmap_from_requirement(req)

    titles = {ticket.title for ticket in roadmap.tickets}
    assert "Implement versioned skill registry with promotion gates" in titles
    assert "Review investment agent console prototype before implementation" in titles

    evolution_ticket = next(ticket for ticket in roadmap.tickets if "skill registry" in ticket.title)
    assert "backtest" in evolution_ticket.gates
    assert "shadow_live" in evolution_ticket.gates
    assert "human_approval" in evolution_ticket.gates

    prototype_ticket = next(ticket for ticket in roadmap.tickets if "prototype" in ticket.title)
    assert "prototype_review" in prototype_ticket.gates


def test_sprint_uses_first_foundation_tickets() -> None:
    req = requirement_from_text("REQ-0001", "Build harness.")
    roadmap = roadmap_from_requirement(req)
    sprint = sprint_from_roadmap(roadmap)

    assert sprint.tickets == ["T-0001", "T-0001A"]
    assert sprint.exit_criteria


def test_default_evaluations_cover_account_and_skill() -> None:
    specs = default_evaluations()
    ids = {spec.id for spec in specs}

    assert "EVAL-ACCOUNT-ALPHA" in ids
    assert "EVAL-SKILL-EVOLUTION" in ids

