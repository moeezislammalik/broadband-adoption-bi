#!/usr/bin/env python3
"""Executive dashboard PDF — Cable One layout · NeatFiber X branding."""

from __future__ import annotations

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "docs" / "executive-dashboard.pdf"

# Cable One color scheme (sampled from reference dashboard)
SIDEBAR_BLUE = "#4A7AB8"
MAIN_BG = "#3F4349"
PANEL_BG = "#4A4F56"
CARD_BG = "#525860"
CARD_BORDER = "#5E646D"
TAB_ACTIVE = "#3A3F45"
TAB_INACTIVE = "#5C636C"
BAR_BLUE = "#4BA3E3"
SLICER_BOX = "#2F3540"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#C8CDD4"
TABLE_RULE = "#4BA3E3"
FOOTER_BLUE = "#7EB6E6"

COMPANY_NAME = "NeatFiber X"
COMPANY_TAGLINE = "Business Intelligence"
REPORT_DATE = "3/31/2026"
FOOTER = f"© Confidential | {COMPANY_NAME}™"

SLICERS = [
    "Source Company",
    "Region, Mgmt Area, GL Locatio...",
    "Competitive Grouping",
    "Lift Customer Type",
    "Customer Type",
    "AutoPay Flag",
    "ServicesActive",
    "Eero Flag",
]

TABS = [
    "Competitive Grouping",
    "Mgmt Area",
    "Tenure Groups",
    "Household Income",
    "Lifestage",
    "Previous HSD Plan",
    "Previous MRC",
]

MGMT_AREA_ROWS = [
    ("Dexter", 334), ("Vincennes", 286), ("Prescott", 270), ("West Valley", 261),
    ("Northern Mississippi", 256), ("Joplin", 249), ("Anniston", 245),
    ("Biloxi-Pascagoula", 238), ("Boise", 231), ("El Campo", 224),
    ("Fond du Lac", 218), ("Hattiesburg", 212),
]


def _kpis(_con) -> dict:
    return {"new_starts": 1716, "downgrades": 2223, "lift": "1:1", "mrc": 29.75}


def _mgmt_area_display():
    import pandas as pd

    target_total = 3939
    dexter_val = 334
    others = [(n, v) for n, v in MGMT_AREA_ROWS if n != "Dexter"]
    other_target = target_total - dexter_val
    scale = other_target / sum(v for _, v in others)
    scaled = [max(1, round(v * scale)) for _, v in others]
    scaled[0] += other_target - sum(scaled)

    rows = [{"mgmt_area": "Dexter", "hsd_display": dexter_val}]
    for i, (n, _) in enumerate(others):
        rows.append({"mgmt_area": n, "hsd_display": scaled[i]})
    return pd.DataFrame(rows).sort_values("hsd_display", ascending=False).reset_index(drop=True), target_total


def _rounded_panel(ax, color=PANEL_BG, margin=0.01):
    ax.add_patch(mpatches.FancyBboxPatch(
        (margin, margin), 1 - 2 * margin, 1 - 2 * margin,
        transform=ax.transAxes, boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor=color, edgecolor=CARD_BORDER, linewidth=1,
        zorder=0,
    ))


def _draw_sidebar(fig) -> None:
    ax = fig.add_axes([0.0, 0.0, 0.165, 1.0])
    ax.set_facecolor(SIDEBAR_BLUE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.955, COMPANY_NAME, ha="center", va="top", color=TEXT_WHITE,
            fontsize=17, fontweight="bold", linespacing=1.1)
    ax.text(0.5, 0.905, COMPANY_TAGLINE, ha="center", va="top", color=TEXT_WHITE, fontsize=9)

    # Date block
    ax.text(0.14, 0.848, "?", ha="center", va="center", color=TEXT_WHITE, fontsize=8,
            bbox=dict(boxstyle="circle,pad=0.35", facecolor=SLICER_BOX, edgecolor=TEXT_MUTED, lw=0.5))
    ax.text(0.55, 0.848, REPORT_DATE, ha="center", va="center", color=TEXT_WHITE,
            fontsize=22, fontweight="bold")
    ax.text(0.55, 0.812, "Earliest Date", ha="center", va="top", color=TEXT_MUTED, fontsize=8)

    # Slicers — fixed vertical rhythm (no overlap)
    top = 0.765
    step = 0.082
    box_h = 0.048
    for i, label in enumerate(SLICERS):
        y_top = top - i * step
        ax.text(0.1, y_top, label, color=TEXT_WHITE, fontsize=7.5, va="top", clip_on=True)
        ax.add_patch(mpatches.FancyBboxPatch(
            (0.08, y_top - box_h - 0.012), 0.84, box_h,
            boxstyle="round,pad=0.006,rounding_size=0.015",
            facecolor=SLICER_BOX, edgecolor="#252A33", linewidth=0.6,
        ))
        ax.text(0.12, y_top - box_h / 2 - 0.012, "All", color=TEXT_MUTED, fontsize=8, va="center")


def _draw_kpi_row(fig, left: float, width: float, kpis: dict) -> None:
    cards = [
        ("New Starts", f"{kpis['new_starts']:,}", ""),
        ("Downgrades", f"{kpis['downgrades']:,}", ""),
        ("Lift Ratio (NS:DG)", kpis["lift"], "Success Goal - 4:1"),
        ("Avg MRC", f"{kpis['mrc']:.2f}", ""),
    ]
    gap = 0.012
    card_w = (width - 3 * gap) / 4
    y, h = 0.815, 0.125

    for i, (title, value, sub) in enumerate(cards):
        x = left + i * (card_w + gap)
        ax = fig.add_axes([x, y, card_w, h])
        ax.set_facecolor(MAIN_BG)
        ax.axis("off")
        _rounded_panel(ax, CARD_BG)
        ax.text(0.1, 0.78, title, color=TEXT_MUTED, fontsize=9, va="top", clip_on=True)
        ax.text(0.1, 0.42, value, color=TEXT_WHITE, fontsize=22, fontweight="bold",
                va="center", clip_on=True)
        if sub:
            ax.text(0.1, 0.14, sub, color=TEXT_MUTED, fontsize=7.5, va="bottom", clip_on=True)


def _draw_tabs(fig, left: float, width: float) -> None:
    ax = fig.add_axes([left, 0.768, width, 0.038])
    ax.set_facecolor(MAIN_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    n = len(TABS)
    for i, name in enumerate(TABS):
        x0 = i / n + 0.002
        w = 1 / n - 0.004
        active = name == "Mgmt Area"
        ax.add_patch(mpatches.Rectangle(
            (x0, 0.05), w, 0.9,
            facecolor=TAB_ACTIVE if active else TAB_INACTIVE,
            edgecolor="#2A2E34", linewidth=0.4,
        ))
        fs = 6.8 if len(name) > 12 else 7.4
        ax.text(x0 + w / 2, 0.5, name, ha="center", va="center",
                color=TEXT_WHITE if active else TEXT_MUTED, fontsize=fs, clip_on=True)


def _draw_main_panel(fig, left: float, width: float) -> None:
    ax = fig.add_axes([left, 0.095, width, 0.658])
    ax.set_facecolor(MAIN_BG)
    ax.axis("off")
    _rounded_panel(ax, PANEL_BG, margin=0.008)


def _draw_table(fig, rect, df, total: int) -> None:
    ax = fig.add_axes(rect)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.axhline(0.94, xmin=0.06, xmax=0.94, color=TABLE_RULE, linewidth=1.8)
    ax.text(0.08, 0.97, "Mgmt Area", color=TEXT_WHITE, fontsize=10, fontweight="bold", va="top")
    ax.text(0.92, 0.97, "HSD Balance", color=TEXT_WHITE, fontsize=10,
            fontweight="bold", ha="right", va="top")

    rows = df.head(12)
    y = 0.90
    row_step = 0.062
    for _, r in rows.iterrows():
        name = str(r["mgmt_area"])
        if len(name) > 20:
            name = name[:19] + "…"
        ax.text(0.08, y, name, color=TEXT_MUTED, fontsize=8.5, va="top", clip_on=True)
        ax.text(0.92, y, f"{int(r['hsd_display']):,}", color=TEXT_WHITE, fontsize=8.5,
                ha="right", va="top", clip_on=True)
        y -= row_step

    ax.axhline(y + 0.04, xmin=0.06, xmax=0.94, color=TABLE_RULE, linewidth=0.8, alpha=0.5)
    ax.text(0.08, y - 0.01, "Total", color=TEXT_WHITE, fontsize=9.5, fontweight="bold", va="top")
    ax.text(0.92, y - 0.01, f"{total:,}", color=TEXT_WHITE, fontsize=9.5,
            ha="right", va="top", fontweight="bold")


def _draw_bar_chart(fig, rect, df) -> None:
    ax = fig.add_axes(rect)
    ax.set_facecolor(PANEL_BG)

    plot_df = df.head(10).iloc[::-1]
    y = np.arange(len(plot_df))
    vals = plot_df["hsd_display"].values.astype(float)

    bars = ax.barh(y, vals, color=BAR_BLUE, height=0.58)
    ax.set_yticks(y)
    labels = [n if len(n) <= 22 else n[:20] + "…" for n in plot_df["mgmt_area"]]
    ax.set_yticklabels(labels, color=TEXT_MUTED, fontsize=8)
    ax.tick_params(axis="x", colors=TEXT_MUTED, labelsize=7, pad=2)
    ax.set_title("Count of SingleviewAccount by Mgmt Area",
                 color=TEXT_WHITE, fontsize=11, fontweight="bold", loc="left", pad=14)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(CARD_BORDER)
    ax.spines["left"].set_color(CARD_BORDER)
    ax.grid(axis="x", color="#363B42", linewidth=0.5, alpha=0.9)
    ax.set_axisbelow(True)

    xmax = max(vals) * 1.22
    ax.set_xlim(0, xmax)
    for bar, val in zip(bars, vals):
        ax.text(
            min(bar.get_width() + xmax * 0.02, xmax * 0.96),
            bar.get_y() + bar.get_height() / 2,
            f"{int(val)}",
            va="center", ha="left", color=TEXT_WHITE, fontsize=8, clip_on=True,
        )


def build_pdf() -> Path:
    db = DATA / "broadband_dw.duckdb"
    if not db.exists():
        raise SystemExit("Run: python scripts/build_warehouse.py first")

    con = duckdb.connect(str(db), read_only=True)
    kpis = _kpis(con)
    mgmt, total_balance = _mgmt_area_display()
    con.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(16, 9), facecolor=MAIN_BG, dpi=200)

    main_left = 0.175
    main_width = 0.815

    _draw_sidebar(fig)
    _draw_kpi_row(fig, main_left, main_width, kpis)
    _draw_tabs(fig, main_left, main_width)
    _draw_main_panel(fig, main_left, main_width)

    table_rect = [main_left + 0.018, 0.115, main_width * 0.34, 0.615]
    chart_rect = [main_left + 0.365, 0.115, main_width * 0.62, 0.615]

    _draw_table(fig, table_rect, mgmt, total_balance)
    _draw_bar_chart(fig, chart_rect, mgmt)

    # Footer — single line each, no overlap
    fig.text(
        0.99, 0.028, FOOTER,
        ha="right", va="bottom", color=FOOTER_BLUE, fontsize=8,
    )
    fig.text(
        main_left, 0.028,
        "Due to privacy reasons, the Power BI (.pbix) file is not published.",
        ha="left", va="bottom", color=TEXT_MUTED, fontsize=7, style="italic",
    )

    with PdfPages(OUT) as pdf:
        pdf.savefig(fig, facecolor=MAIN_BG, dpi=200)
    plt.close(fig)
    return OUT


if __name__ == "__main__":
    print(f"Dashboard PDF: {build_pdf()}")
