from __future__ import annotations

from datetime import date, timedelta

from .models import EvaluationSpec, Gate, Requirement, RiskLevel, Roadmap, SprintPlan, Ticket


def requirement_from_text(requirement_id: str, text: str) -> Requirement:
    return Requirement(
        id=requirement_id,
        title="Self-Evolving Investment Agent",
        problem=text,
        target_users=[
            "individual investors",
            "small investment research teams",
            "quantitative strategy researchers",
        ],
        outcomes=[
            "Engineering work is traceable from requirement to ticket to verification",
            "Investment hypotheses, trade plans, account performance, and reviews are recorded structurally",
            "Agent and skill improvements must pass evaluation gates before promotion",
        ],
        scope=[
            "structured requirement intake",
            "roadmap decomposition and sprint planning",
            "account profitability evaluation",
            "controlled self-evolution evaluation",
            "local test and CI baseline",
        ],
        non_goals=[
            "Do not enable live automated trading by default in the first phase",
            "Do not perform online model-weight self-training in the first phase",
        ],
        risks=[
            "Free market data sources may be unstable",
            "AI investment judgments may be hard to explain or review",
            "Strategies may overfit historical regimes",
            "Automated evolution may accidentally weaken high-risk trading logic",
        ],
        acceptance_criteria=[
            "A raw requirement can produce a structured requirement artifact",
            "The harness can generate gated engineering tickets",
            "Core workflow documents and evaluation specs can be validated",
            "Local checks pass consistently",
        ],
    )


def roadmap_from_requirement(req: Requirement) -> Roadmap:
    milestones = [
        "M1 Harness Foundation",
        "M2 Investment Ledger Core",
        "M3 Profitability Evaluation",
        "M4 Skill Evolution Loop",
        "M5 Shadow Trading and Promotion Gates",
    ]
    tickets = [
        Ticket(
            id="T-0001",
            title="Create engineering harness CLI and artifact layout",
            requirement_id=req.id,
            milestone=milestones[0],
            description="Provide commands for requirement intake, planning, validation, and eval generation.",
            risk_level=RiskLevel.low,
            gates=[Gate.requirement_review, Gate.unit_tests],
            deliverables=["CLI", "README", "tests"],
        ),
        Ticket(
            id="T-0002",
            title="Define hypothesis, plan, event, result, and review ledgers",
            requirement_id=req.id,
            milestone=milestones[1],
            description="Specify the canonical investment ledger schemas for replayable decisions.",
            risk_level=RiskLevel.medium,
            gates=[Gate.requirement_review, Gate.design_review, Gate.unit_tests],
            deliverables=["ledger schema", "sample records", "validation tests"],
        ),
        Ticket(
            id="T-0003",
            title="Build account and agent profitability attribution model",
            requirement_id=req.id,
            milestone=milestones[2],
            description="Separate market beta, strategy contribution, agent contribution, and user execution impact.",
            risk_level=RiskLevel.high,
            gates=[Gate.design_review, Gate.integration_tests, Gate.data_quality],
            deliverables=["evaluation spec", "metric definitions", "fixture portfolio"],
        ),
        Ticket(
            id="T-0004",
            title="Implement versioned skill registry with promotion gates",
            requirement_id=req.id,
            milestone=milestones[3],
            description="Track candidate/backtested/shadow_live/active/retired skill lifecycle states.",
            risk_level=RiskLevel.high,
            gates=[
                Gate.unit_tests,
                Gate.backtest,
                Gate.shadow_live,
                Gate.human_approval,
                Gate.rollback_plan,
            ],
            deliverables=["skill schema", "promotion policy", "rollback policy"],
        ),
        Ticket(
            id="T-0005",
            title="Create shadow portfolio evaluation loop",
            requirement_id=req.id,
            milestone=milestones[4],
            description="Compare actual account, agent-advised portfolio, strategy portfolio, and benchmark.",
            risk_level=RiskLevel.critical,
            gates=[
                Gate.integration_tests,
                Gate.data_quality,
                Gate.shadow_live,
                Gate.human_approval,
                Gate.rollback_plan,
            ],
            deliverables=["shadow portfolio spec", "daily review job", "promotion report"],
        ),
    ]
    return Roadmap(requirement_id=req.id, milestones=milestones, tickets=tickets)


def sprint_from_roadmap(roadmap: Roadmap) -> SprintPlan:
    today = date.today()
    first_two = [ticket.id for ticket in roadmap.tickets[:2]]
    return SprintPlan(
        id="SPRINT-0001",
        starts_on=today,
        ends_on=today + timedelta(days=14),
        goals=[
            "Make the engineering harness runnable end to end",
            "Lock the ledger schema needed for reviewable investment decisions",
        ],
        tickets=first_two,
        exit_criteria=[
            "CLI intake, plan, and validate commands pass locally",
            "Initial ledger and evolution specs are reviewed",
            "Unit tests pass",
        ],
    )


def default_evaluations() -> list[EvaluationSpec]:
    return [
        EvaluationSpec(
            id="EVAL-ACCOUNT-ALPHA",
            name="Account Profitability Attribution",
            objective="Measure whether the agent improves account outcomes after separating market movement and user execution.",
            metrics=[
                "total_return",
                "benchmark_excess_return",
                "max_drawdown",
                "sharpe_ratio",
                "calmar_ratio",
                "win_rate",
                "profit_factor",
                "agent_contribution",
                "user_execution_drag",
            ],
            data_sources=["positions", "orders", "benchmarks", "agent_recommendations", "market_bars"],
            cadence="daily_close_and_weekly_review",
            promotion_rules=[
                "Agent-advised shadow portfolio outperforms benchmark over the evaluation window",
                "Drawdown does not exceed approved risk budget",
                "Confidence calibration error improves or remains stable",
            ],
            rollback_rules=[
                "Excess drawdown breaches limit",
                "Signal false-positive rate exceeds threshold",
                "User override success rate is materially higher than agent acceptance success rate",
            ],
        ),
        EvaluationSpec(
            id="EVAL-SKILL-EVOLUTION",
            name="Skill Evolution Gate",
            objective="Promote only skill versions that prove better through backtest and shadow-live evidence.",
            metrics=[
                "hit_rate_by_horizon",
                "excess_return_by_horizon",
                "max_adverse_excursion",
                "false_positive_rate",
                "signal_frequency",
                "market_regime_coverage",
                "rollback_rate",
            ],
            data_sources=["hypothesis_ledger", "review_ledger", "skill_versions", "backtest_results"],
            cadence="weekly_or_after_30_new_signals",
            promotion_rules=[
                "Candidate skill beats active version on primary metric",
                "Candidate skill does not worsen max drawdown",
                "Candidate skill passes at least one out-of-sample market regime",
                "High-risk changes require human approval",
            ],
            rollback_rules=[
                "Shadow-live performance falls below active skill",
                "Market regime detector marks the skill out of scope",
                "Risk agent flags a repeated failure mode",
            ],
        ),
    ]
