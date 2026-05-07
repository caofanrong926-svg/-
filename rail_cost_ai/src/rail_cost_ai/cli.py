from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import calc_category_share, calc_unit_cost_per_km, compare_with_history
from .excel_parser import parse_summary_excel
from .history_db import append_history, init_history_db, read_history
from .report_exporter import export_excel_report, export_word_report


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="轨道交通造价AI分析工具")
    p.add_argument("--input", required=True, help="输入综合概算表Excel")
    p.add_argument("--history", default="data/history_projects.xlsx", help="历史指标库文件")
    p.add_argument("--output-dir", default="output", help="输出目录")
    p.add_argument("--no-append-history", action="store_true", help="不写入历史库")
    return p


def main() -> None:
    args = build_parser().parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    init_history_db(args.history)

    project, cost_items = parse_summary_excel(args.input)
    unit_cost = calc_unit_cost_per_km(project)
    category_share_rows = calc_category_share(cost_items, project.total_investment_million)

    history_rows = read_history(args.history)
    comparisons = compare_with_history(project, history_rows)

    excel_out = output_dir / f"{project.project_name}_分析结果.xlsx"
    word_out = output_dir / f"{project.project_name}_分析报告.docx"

    export_excel_report(project, cost_items, category_share_rows, comparisons, excel_out)
    export_word_report(project, unit_cost, category_share_rows, comparisons, word_out)

    if not args.no_append_history:
        append_history(project, args.history)

    print(f"分析完成：\n- Excel: {excel_out}\n- Word: {word_out}")


if __name__ == "__main__":
    main()
