from __future__ import annotations

from pathlib import Path

import pandas as pd

from .analyzer import calc_unit_cost_per_km
from .models import ProjectInfo


HISTORY_COLUMNS = [
    "project_name",
    "line_length_km",
    "station_count",
    "total_investment_million",
    "unit_cost_per_km",
]


def init_history_db(history_file: str | Path) -> None:
    path = Path(history_file)
    if not path.exists():
        df = pd.DataFrame(columns=HISTORY_COLUMNS)
        df.to_excel(path, index=False)


def read_history(history_file: str | Path) -> list[dict]:
    path = Path(history_file)
    if not path.exists():
        return []
    df = pd.read_excel(path)
    if df.empty:
        return []
    return df.fillna(0).to_dict(orient="records")


def append_history(project: ProjectInfo, history_file: str | Path) -> None:
    init_history_db(history_file)
    df = pd.read_excel(history_file)
    row = {
        "project_name": project.project_name,
        "line_length_km": project.line_length_km,
        "station_count": project.station_count,
        "total_investment_million": project.total_investment_million,
        "unit_cost_per_km": calc_unit_cost_per_km(project),
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(history_file, index=False)
