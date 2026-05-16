# Harness Maturity Model

The harness should mature in levels. Do not skip levels for high-risk investment functionality.

## Level 0: Ad Hoc

- Ideas are discussed in chat.
- Code is changed directly.
- Tests are optional.
- No durable trace connects decisions to outcomes.

This level is not acceptable for investment-agent work.

## Level 1: Traceable Planning

- Requirements are structured.
- Roadmaps and sprint plans exist.
- Basic CI runs lint and tests.
- ADRs capture important decisions.

Current baseline target.

## Level 2: Quality-Gated Delivery

- Every ticket declares gates.
- Test plans exist for risky work.
- CI blocks broken changes.
- Release checklists and rollback plans exist.

Near-term target.

## Level 3: Evaluation-Gated Agent Work

- Agent recommendations are recorded as hypotheses.
- Account alpha and skill evolution are evaluated.
- Shadow portfolios compare agent, strategy, user, and benchmark outcomes.
- Skill promotion requires evidence.

Investment-agent MVP target.

## Level 4: Controlled Evolution

- Runtime traces feed review and learning.
- Candidate skills/configs are generated offline.
- Backtest and shadow-live decide promotion.
- Rollback and drift monitoring are standard.

Self-evolving agent target.

## Level 5: Governed Autonomy

- Low-risk improvements can auto-promote.
- High-risk changes require approval.
- Release, monitoring, and rollback are automated.
- Governance metrics are reviewed regularly.

Long-term target.

