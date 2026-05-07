from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .models import CostItem, ProjectInfo


KEYWORDS = {
    "project_name": ["项目名称", "项目", "工程名称"],
    "line_length": ["线路长度", "长度", "正线长度"],
    "station_count": ["车站数量", "车站数", "站点数量"],
    "total_investment": ["总投资", "投资总额", "总概算"],
}


def _extract_number(text: object) -> float | None:
    if text is None:
        return None
    found = re.findall(r"-?\d+(?:\.\d+)?", str(text).replace(",", ""))
    return float(found[0]) if found else None


def _find_by_keywords(df: pd.DataFrame, keywords: list[str]) -> float | str | None:
    for row in df.itertuples(index=False):
        cells = ["" if pd.isna(v) else str(v) for v in row]
        for idx, cell in enumerate(cells):
            if any(k in cell for k in keywords):
                if idx + 1 < len(cells) and cells[idx + 1].strip():
                    right_value = cells[idx + 1].strip()
                    return _extract_number(right_value) or right_value
                numeric_candidates = [_extract_number(c) for c in cells if _extract_number(c) is not None]
                if numeric_candidates:
                    return numeric_candidates[-1]
    return None


def parse_summary_excel(path: str | Path) -> tuple[ProjectInfo, list[CostItem]]:
    sheets = pd.read_excel(path, sheet_name=None, header=None)
    all_df = pd.concat(sheets.values(), ignore_index=True)

    project_name = _find_by_keywords(all_df, KEYWORDS["project_name"])
    line_length = _find_by_keywords(all_df, KEYWORDS["line_length"])
    station_count = _find_by_keywords(all_df, KEYWORDS["station_count"])
    total_investment = _find_by_keywords(all_df, KEYWORDS["total_investment"])

    if not isinstance(project_name, str):
        project_name = Path(path).stem

    info = ProjectInfo(
        project_name=project_name,
        line_length_km=float(line_length or 0),
        station_count=int(float(station_count or 0)),
        total_investment_million=float(total_investment or 0),
    )

    cost_items: list[CostItem] = []
    for _, row in all_df.iterrows():
        if len(row) < 2:
            continue
        category = row.iloc[0]
        amount = _extract_number(row.iloc[1])
        if isinstance(category, str) and amount is not None:
            if any(x in category for x in ["费", "工程", "设备", "其他"]):
                cost_items.append(CostItem(category=category.strip(), amount_million=amount))

    dedup: dict[str, float] = {}
    for item in cost_items:
        dedup[item.category] = max(dedup.get(item.category, 0), item.amount_million)
    normalized = [CostItem(category=k, amount_million=v) for k, v in dedup.items()]
    return info, normalized
