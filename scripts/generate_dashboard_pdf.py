#!/usr/bin/env python3
"""Generate executive dashboard PDF (portfolio deliverable)."""

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

BG = "#1B2838"
CARD = "#243447"
ACCENT = "#3B82F6"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
GRID = "#334155"


def _load_kpis(con: duckdb.DuckDBPyConnection) -> dict:
    row = con.execute(
        """
        SELECT
            ROUND(100.0 * SUM(households_adopted) / SUM(households_total), 2),
            ROUND(100.0 * AVG(penetration_rate), 2),
            ROUND(100.0 * AVG(penetration_gap), 2),
            SUM(new_starts),
            SUM(downgrades),
            ROUND(AVG(avg_mrc_usd), 2)
        FROM fact_broadband_adoption f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.is_current_quarter
        """
    ).fetchone()
    lift = row[3] / row[4] if row[4] else 0
    return {
        "adoption": row[0],
        "penetration": row[1],
        "gap": row[2],
        "new_starts": int(row[3]),
        "downgrades": int(row[4]),
        "lift": f"1:{round(row[4]/row[3], 1)}" if row[3] else "—",
        "mrc": row[5],
    }


def _state_adoption(con: duckdb.DuckDBPyConnection):
    return con.execute(
        """
        SELECT s.state_name,
               ROUND(100.0 * SUM(f.households_adopted) / SUM(f.households_total), 2) AS adoption_pct
        FROM fact_broadband_adoption f
        JOIN dim_state s ON f.state_key = s.state_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.is_current_quarter
        GROUP BY s.state_name
        ORDER BY adoption_pct DESC
        """
    ).fetchdf()


def _trend(con: duckdb.DuckDBPyConnection):
    return con.execute(
        """
        SELECT d.year_quarter,
               ROUND(100.0 * SUM(f.households_adopted) / SUM(f.households_total), 2) AS adoption_pct,
               ROUND(100.0 * AVG(f.penetration_rate), 2) AS penetration_pct
        FROM fact_broadband_adoption f
        JOIN dim_date d ON f.date_key = d.date_key
        GROUP BY d.year_quarter, d.date_key
        ORDER BY d.date_key
        """
    ).fetchdf()


def _tech_adoption(con: duckdb.DuckDBPyConnection):
    return con.execute(
        """
        SELECT t.technology_name,
               ROUND(100.0 * SUM(f.households_adopted) / SUM(f.households_total), 2) AS adoption_pct
        FROM fact_broadband_adoption f
        JOIN dim_technology t ON f.technology_key = t.technology_key
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.is_current_quarter
        GROUP BY t.technology_name
        ORDER BY adoption_pct DESC
        """
    ).fetchdf()


def _yoy(con: duckdb.DuckDBPyConnection) -> float:
    rows = con.execute(
        """
        SELECT d.year,
               ROUND(100.0 * SUM(f.households_adopted) / SUM(f.households_total), 2) AS rate
        FROM fact_broadband_adoption f
        JOIN dim_date d ON f.date_key = d.date_key
        WHERE d.quarter = 1
        GROUP BY d.year
        ORDER BY d.year
        """
    ).fetchall()
    if len(rows) >= 2:
        return round(rows[-1][1] - rows[-2][1], 2)
    return 0.0


def _kpi_card(ax, title: str, value: str, subtitle: str = "") -> None:
    ax.set_facecolor(CARD)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for spine in ax.spines.values():
        spine.set_visible(False)
    rect = mpatches.FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.9, boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1, edgecolor=GRID, facecolor=CARD
    )
    ax.add_patch(rect)
    ax.text(0.08, 0.72, title, color=MUTED, fontsize=9, fontweight="medium", va="top")
    ax.text(0.08, 0.42, value, color=TEXT, fontsize=22, fontweight="bold", va="center")
    if subtitle:
        ax.text(0.08, 0.18, subtitle, color=MUTED, fontsize=8, va="bottom")


def build_pdf() -> Path:
    db = DATA / "broadband_dw.duckdb"
    if not db.exists():
        raise SystemExit("Run: python scripts/build_warehouse.py first")

    con = duckdb.connect(str(db), read_only=True)
    kpis = _load_kpis(con)
    kpis["yoy"] = _yoy(con)
    states = _state_adoption(con)
    trend = _trend(con)
    tech = _tech_adoption(con)
    con.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(OUT) as pdf:
        # ── Page 1: Executive State View ─────────────────────────────────────
        fig = plt.figure(figsize=(16, 9), facecolor=BG)
        fig.suptitle(
            "Broadband Adoption Executive Portal",
            color=TEXT, fontsize=18, fontweight="bold", y=0.97, x=0.32,
        )
        fig.text(
            0.32, 0.935,
            "March 2026 · 24 States · Adoption · Penetration · Trend Monitoring  |  Synthetic portfolio data",
            color=MUTED, fontsize=9,
        )
        fig.text(
            0.02, 0.02,
            "Due to privacy reasons, the live Power BI (.pbix) file is not published. "
            "This PDF is the executive dashboard deliverable.",
            color=MUTED, fontsize=7.5, style="italic",
        )

        # KPI row
        kpi_titles = [
            ("Adoption Rate", f"{kpis['adoption']}%", f"YoY {kpis['yoy']:+.1f} pp"),
            ("Penetration Rate", f"{kpis['penetration']}%", "Service reach index"),
            ("Penetration Gap", f"{kpis['gap']}%", "Upsell opportunity"),
            ("New Starts", f"{kpis['new_starts']:,}", "Current quarter"),
            ("Downgrades", f"{kpis['downgrades']:,}", f"Lift {kpis['lift']} · Goal 4:1"),
            ("Avg MRC", f"${kpis['mrc']}", "Monthly recurring charge"),
        ]
        for i, (t, v, s) in enumerate(kpi_titles):
            ax = fig.add_axes([0.02 + i * 0.16, 0.78, 0.14, 0.14])
            _kpi_card(ax, t, v, s)

        # Filter panel (decorative labels — PDF static)
        ax_f = fig.add_axes([0.02, 0.12, 0.14, 0.62])
        ax_f.set_facecolor(CARD)
        ax_f.axis("off")
        ax_f.text(0.1, 0.95, "FILTERS", color=TEXT, fontsize=10, fontweight="bold")
        filters = ["State (24)", "Region", "Income Bracket", "Market Type",
                   "Technology", "Provider", "Year", "Quarter"]
        for j, f in enumerate(filters):
            ax_f.add_patch(mpatches.FancyBboxPatch(
                (0.05, 0.82 - j * 0.1), 0.9, 0.07,
                boxstyle="round,pad=0.01", facecolor=BG, edgecolor=GRID, linewidth=0.8
            ))
            ax_f.text(0.12, 0.855 - j * 0.1, f, color=MUTED, fontsize=7, va="center")

        # State table
        ax_t = fig.add_axes([0.19, 0.14, 0.22, 0.58])
        ax_t.set_facecolor(CARD)
        ax_t.axis("off")
        ax_t.set_title("State · Adoption %", color=TEXT, fontsize=10, loc="left", pad=8)
        top = states.head(12)
        for j, (_, r) in enumerate(top.iterrows()):
            ax_t.text(0.02, 0.88 - j * 0.07, r["state_name"][:14], color=MUTED, fontsize=7.5)
            ax_t.text(0.92, 0.88 - j * 0.07, f"{r['adoption_pct']:.1f}%",
                      color=ACCENT, fontsize=7.5, ha="right", fontweight="bold")

        # Horizontal bar chart
        ax_b = fig.add_axes([0.44, 0.14, 0.54, 0.58])
        ax_b.set_facecolor(CARD)
        plot_states = states.head(14).iloc[::-1]
        y = np.arange(len(plot_states))
        bars = ax_b.barh(y, plot_states["adoption_pct"], color=ACCENT, height=0.65)
        ax_b.set_yticks(y)
        ax_b.set_yticklabels(plot_states["state_name"], color=MUTED, fontsize=8)
        ax_b.set_xlabel("Adoption Rate %", color=MUTED, fontsize=8)
        ax_b.tick_params(axis="x", colors=MUTED)
        ax_b.set_title("Adoption Rate by State (Current Quarter)", color=TEXT, fontsize=11, pad=10)
        for spine in ax_b.spines.values():
            spine.set_color(GRID)
        ax_b.grid(axis="x", color=GRID, alpha=0.4, linestyle="--")
        for bar, val in zip(bars, plot_states["adoption_pct"]):
            ax_b.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                      f"{val:.1f}%", va="center", color=TEXT, fontsize=7)

        # Tabs
        ax_tabs = fig.add_axes([0.19, 0.74, 0.79, 0.03])
        ax_tabs.set_facecolor(BG)
        ax_tabs.axis("off")
        tabs = ["State View", "Income Bracket", "Urban vs Rural", "Technology", "Trend"]
        for i, tab in enumerate(tabs):
            c = ACCENT if tab == "State View" else GRID
            fc = CARD if tab == "State View" else BG
            ax_tabs.add_patch(mpatches.FancyBboxPatch(
                (i * 0.2, 0.1), 0.18, 0.8, boxstyle="round,pad=0.02",
                facecolor=fc, edgecolor=c, linewidth=1
            ))
            ax_tabs.text(i * 0.2 + 0.09, 0.5, tab, ha="center", va="center",
                         color=TEXT if tab == "State View" else MUTED, fontsize=8)

        pdf.savefig(fig, facecolor=BG)
        plt.close(fig)

        # ── Page 2: Trend + Technology ───────────────────────────────────────
        fig2 = plt.figure(figsize=(16, 9), facecolor=BG)
        fig2.suptitle(
            "Broadband Adoption Executive Portal — Trend & Technology",
            color=TEXT, fontsize=16, fontweight="bold", y=0.96, x=0.28,
        )

        ax_line = fig2.add_axes([0.06, 0.48, 0.88, 0.42])
        ax_line.set_facecolor(CARD)
        ax_line.plot(trend["year_quarter"], trend["adoption_pct"],
                     color=ACCENT, marker="o", linewidth=2, label="Adoption %")
        ax_line.plot(trend["year_quarter"], trend["penetration_pct"],
                     color="#60A5FA", marker="s", linewidth=2, linestyle="--", label="Penetration %")
        ax_line.set_title("Quarterly Adoption & Penetration Trend", color=TEXT, fontsize=12, pad=12)
        ax_line.tick_params(axis="both", colors=MUTED, labelsize=8)
        ax_line.set_xticks(range(len(trend)))
        ax_line.set_xticklabels(trend["year_quarter"], rotation=45, ha="right")
        ax_line.legend(facecolor=CARD, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
        ax_line.grid(color=GRID, alpha=0.35, linestyle="--")
        for spine in ax_line.spines.values():
            spine.set_color(GRID)

        ax_tech = fig2.add_axes([0.06, 0.08, 0.42, 0.34])
        ax_tech.set_facecolor(CARD)
        x = np.arange(len(tech))
        ax_tech.bar(x, tech["adoption_pct"], color=[ACCENT, "#60A5FA", "#93C5FD", "#2563EB"][: len(tech)])
        ax_tech.set_xticks(x)
        ax_tech.set_xticklabels(tech["technology_name"], color=MUTED, fontsize=9)
        ax_tech.set_ylabel("Adoption %", color=MUTED, fontsize=9)
        ax_tech.set_title("Adoption by Technology (Current Quarter)", color=TEXT, fontsize=11)
        ax_tech.tick_params(axis="y", colors=MUTED)
        for spine in ax_tech.spines.values():
            spine.set_color(GRID)

        ax_note = fig2.add_axes([0.52, 0.08, 0.42, 0.34])
        ax_note.set_facecolor(CARD)
        ax_note.axis("off")
        notes = [
            "STAR-SCHEMA DESIGN",
            "• dim_date · dim_state (24) · dim_segment",
            "• dim_technology · dim_provider",
            "• fact_broadband_adoption",
            "",
            "PRIVACY & DELIVERABLE",
            "• No employer / operator branding",
            "• Power BI source file withheld",
            "• PDF provided for portfolio review",
            "",
            f"Records analyzed: 2M+ transaction grain",
            f"States in scope: 24",
        ]
        for j, line in enumerate(notes):
            color = TEXT if line.isupper() and "·" not in line and not line.startswith("•") else MUTED
            weight = "bold" if line.isupper() and not line.startswith("•") and line else "normal"
            ax_note.text(0.06, 0.92 - j * 0.08, line, color=color, fontsize=9,
                         fontweight=weight, va="top", family="sans-serif")

        pdf.savefig(fig2, facecolor=BG)
        plt.close(fig2)

    return OUT


if __name__ == "__main__":
    path = build_pdf()
    print(f"Dashboard PDF: {path}")
