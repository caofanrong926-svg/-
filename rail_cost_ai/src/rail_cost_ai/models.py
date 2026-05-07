from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProjectInfo:
    project_name: str
    line_length_km: float
    station_count: int
    total_investment_million: float


@dataclass
class CostItem:
    category: str
    amount_million: float


@dataclass
class ComparisonResult:
    project_name: str
    total_investment_million: float
    unit_cost_per_km: float
    deviation_rate_pct: float
