from __future__ import annotations

from .models import ComparisonResult, CostItem, ProjectInfo


def calc_unit_cost_per_km(project: ProjectInfo) -> float:
    if project.line_length_km <= 0:
        return 0.0
    return project.total_investment_million / project.line_length_km


def calc_category_share(cost_items: list[CostItem], total_investment_million: float) -> list[dict]:
    if total_investment_million <= 0:
        return [{"category": c.category, "amount": c.amount_million, "share_pct": 0.0} for c in cost_items]
    return [
        {
            "category": c.category,
            "amount": c.amount_million,
            "share_pct": c.amount_million / total_investment_million * 100,
        }
        for c in cost_items
    ]


def compare_with_history(current: ProjectInfo, history_rows: list[dict]) -> list[ComparisonResult]:
    current_unit = calc_unit_cost_per_km(current)
    results: list[ComparisonResult] = []
    for row in history_rows:
        hist_unit = float(row["unit_cost_per_km"])
        deviation = ((current_unit - hist_unit) / hist_unit * 100) if hist_unit else 0.0
        results.append(
            ComparisonResult(
                project_name=row["project_name"],
                total_investment_million=float(row["total_investment_million"]),
                unit_cost_per_km=hist_unit,
                deviation_rate_pct=deviation,
            )
        )
    return sorted(results, key=lambda x: abs(x.deviation_rate_pct))
