#!/usr/bin/env python3
"""Generate star-schema CSVs for 24-state broadband adoption model."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 2026

STATES = [
    ("AL", "Alabama"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CO", "Colorado"),
    ("GA", "Georgia"), ("ID", "Idaho"), ("IA", "Iowa"), ("KS", "Kansas"),
    ("KY", "Kentucky"), ("LA", "Louisiana"), ("MN", "Minnesota"), ("MS", "Mississippi"),
    ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"),
    ("NM", "New Mexico"), ("NC", "North Carolina"), ("OK", "Oklahoma"), ("SC", "South Carolina"),
    ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("WI", "Wisconsin"),
]

SEGMENTS = [
    ("URBAN", "Urban", "Metro"),
    ("SUBURB", "Suburban", "Metro"),
    ("RURAL", "Rural", "Non-Metro"),
    ("LOW_INC", "Low Income", "All"),
    ("MID_INC", "Middle Income", "All"),
    ("HIGH_INC", "High Income", "All"),
]

TECH = [
    ("FIBER", "Fiber"),
    ("CABLE", "Cable"),
    ("DSL", "DSL"),
    ("FWA", "Fixed Wireless"),
]

PROVIDERS = [
    ("PRV01", "Regional Fiber Co"),
    ("PRV02", "National Cable Group"),
    ("PRV03", "Rural Connect LLC"),
    ("PRV04", "Metro Broadband Inc"),
]


def dim_date() -> pd.DataFrame:
    dates = pd.date_range("2023-01-01", "2026-03-31", freq="MS")
    df = pd.DataFrame({"date": dates})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["year_quarter"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)
    df["month_name"] = df["date"].dt.strftime("%b %Y")
    df["is_current_quarter"] = df["year_quarter"] == "2026 Q1"
    return df


def dim_state() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for code, name in STATES:
        base = rng.uniform(0.62, 0.91)
        rows.append(
            {
                "state_key": code,
                "state_name": name,
                "region": rng.choice(["Northeast", "South", "Midwest", "West"]),
                "population_k": int(rng.integers(600, 12000)),
                "target_penetration_pct": round(base * 100, 1),
            }
        )
    return pd.DataFrame(rows)


def dim_segment() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "segment_key": k,
                "segment_name": n,
                "market_type": m,
                "income_bracket": (
                    "Low" if "LOW" in k else "Middle" if "MID" in k else "High" if "HIGH" in k else "All"
                ),
            }
            for k, n, m in SEGMENTS
        ]
    )


def dim_technology() -> pd.DataFrame:
    return pd.DataFrame(
        [{"technology_key": k, "technology_name": n, "speed_tier": t} for k, n, t in [
            ("FIBER", "Fiber", "1 Gbps+"),
            ("CABLE", "Cable", "500 Mbps"),
            ("DSL", "DSL", "100 Mbps"),
            ("FWA", "Fixed Wireless", "300 Mbps"),
        ]]
    )


def dim_provider() -> pd.DataFrame:
    return pd.DataFrame(
        [{"provider_key": k, "provider_name": n} for k, n in PROVIDERS]
    )


def fact_broadband_adoption(dates: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    date_keys = dates["date_key"].tolist()
    for _, st in states.iterrows():
        state_pen = st["target_penetration_pct"] / 100
        trend = rng.uniform(-0.004, 0.012, len(date_keys)).cumsum()
        for i, dk in enumerate(date_keys):
            for seg_key, _, _ in SEGMENTS:
                for tech_key, _ in TECH:
                    for prv_key, _ in PROVIDERS:
                        if rng.random() > 0.35:
                            continue
                        households = int(rng.integers(8000, 120000))
                        adoption = np.clip(
                            state_pen
                            + trend[i]
                            + (0.08 if tech_key == "FIBER" else -0.03 if tech_key == "DSL" else 0)
                            + (0.05 if "HIGH" in seg_key else -0.06 if "LOW" in seg_key else 0)
                            + rng.normal(0, 0.02),
                            0.35,
                            0.98,
                        )
                        penetration = np.clip(adoption + rng.uniform(0.02, 0.12), adoption, 0.99)
                        adopted_hh = int(households * adoption)
                        rows.append(
                            {
                                "date_key": dk,
                                "state_key": st["state_key"],
                                "segment_key": seg_key,
                                "technology_key": tech_key,
                                "provider_key": prv_key,
                                "households_total": households,
                                "households_adopted": adopted_hh,
                                "adoption_rate": round(adoption, 4),
                                "penetration_rate": round(penetration, 4),
                                "penetration_gap": round(penetration - adoption, 4),
                                "avg_mrc_usd": round(rng.uniform(39, 89), 2),
                                "new_starts": int(rng.integers(120, 2400)),
                                "downgrades": int(rng.integers(80, 1800)),
                            }
                        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    d_date = dim_date()
    d_state = dim_state()
    d_segment = dim_segment()
    d_tech = dim_technology()
    d_provider = dim_provider()
    fact = fact_broadband_adoption(d_date, d_state)

    d_date.to_csv(DATA / "dim_date.csv", index=False)
    d_state.to_csv(DATA / "dim_state.csv", index=False)
    d_segment.to_csv(DATA / "dim_segment.csv", index=False)
    d_tech.to_csv(DATA / "dim_technology.csv", index=False)
    d_provider.to_csv(DATA / "dim_provider.csv", index=False)
    fact.to_csv(DATA / "fact_broadband_adoption.csv", index=False)

    print(f"Generated {len(fact):,} fact rows across {len(STATES)} states.")


if __name__ == "__main__":
    main()
