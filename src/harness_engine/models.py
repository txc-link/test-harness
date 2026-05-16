from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Gate(str, Enum):
    requirement_review = "requirement_review"
    design_review = "design_review"
    unit_tests = "unit_tests"
    integration_tests = "integration_tests"
    data_quality = "data_quality"
    backtest = "backtest"
    shadow_live = "shadow_live"
    human_approval = "human_approval"
    rollback_plan = "rollback_plan"


class Requirement(BaseModel):
    id: str
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    problem: str
    target_users: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    scope: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)


class Ticket(BaseModel):
    id: str
    title: str
    requirement_id: str
    milestone: str
    description: str
    owner: str = "agent"
    risk_level: RiskLevel = RiskLevel.medium
    gates: list[Gate] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)


class Roadmap(BaseModel):
    requirement_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    milestones: list[str]
    tickets: list[Ticket]


class EvaluationSpec(BaseModel):
    id: str
    name: str
    objective: str
    metrics: list[str]
    data_sources: list[str]
    cadence: str
    promotion_rules: list[str]
    rollback_rules: list[str]


class SprintPlan(BaseModel):
    id: str
    starts_on: date
    ends_on: date
    goals: list[str]
    tickets: list[str]
    exit_criteria: list[str]


class HarnessCheck(BaseModel):
    name: str
    passed: bool
    detail: str


class HarnessStatus(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    maturity_level: int
    checks: list[HarnessCheck]


class ReleaseRecord(BaseModel):
    id: str
    title: str
    status: str = "draft"
    scope: list[str] = Field(default_factory=list)
    included_tickets: list[str] = Field(default_factory=list)
    validation: list[str] = Field(default_factory=list)
    rollback_plan: list[str] = Field(default_factory=list)
    monitoring_plan: list[str] = Field(default_factory=list)
