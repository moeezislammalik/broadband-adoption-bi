#!/usr/bin/env python3
"""Load star-schema CSVs into DuckDB warehouse for validation."""

import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "broadband_dw.duckdb"

TABLES = [
    "dim_date",
    "dim_state",
    "dim_segment",
    "dim_technology",
    "dim_provider",
    "fact_broadband_adoption",
]


def main() -> None:
    if not (DATA / "fact_broadband_adoption.csv").exists():
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_data.py")], check=True)

    DB.unlink(missing_ok=True)
    con = duckdb.connect(str(DB))

    for table in TABLES:
        path = DATA / f"{table}.csv"
        con.execute(
            f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{path.as_posix()}');"
        )

    views = (ROOT / "sql" / "executive_kpi_views.sql").read_text()
    for stmt in views.split(";"):
        stmt = stmt.strip()
        if stmt:
            con.execute(stmt)

    row = con.execute(
        """
        SELECT ROUND(AVG(adoption_rate_pct), 2), ROUND(AVG(penetration_rate_pct), 2)
        FROM vw_executive_kpi
        WHERE is_current_quarter
        """
    ).fetchone()
    print(f"Warehouse ready: {DB}")
    print(f"Current-quarter avg adoption: {row[0]}% | penetration: {row[1]}%")


if __name__ == "__main__":
    main()
