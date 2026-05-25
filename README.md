# Broadband Adoption Executive BI

**March 2026** · Power BI · Star-schema · 24 states

**[Project Link](https://github.com/moeezislammalik/broadband-adoption-bi)**

De-identified **Power BI suite** with a **star-schema** data model for **broadband adoption** across **24 states**. Includes executive views for **adoption rate**, **penetration**, **penetration gap**, and **YoY trend monitoring** — built to a professional executive dashboard standard (dark theme, KPI scorecards, slicers, tabbed analysis).

> Privacy: No real company or employer names appear in this repository. All states, providers, and metrics are synthetic portfolio data.

---

## Portfolio summary

- Designed a **star-schema** warehouse (`dim_*` + `fact_broadband_adoption`) for multi-state broadband KPIs
- Built **executive Power BI views** — adoption rate, penetration, gap analysis, and trend monitoring
- Delivered **DAX measure library**, Power Query templates, SQL views, and dashboard specification for reproducible BI development

---

## Star schema

| Table | Role |
|-------|------|
| `dim_date` | Time intelligence (YoY, quarters) |
| `dim_state` | 24-state geography + targets |
| `dim_segment` | Income & urban/suburban/rural |
| `dim_technology` | Fiber, cable, DSL, fixed wireless |
| `dim_provider` | De-identified service providers |
| `fact_broadband_adoption` | Households, adoption, penetration, MRC, starts/downgrades |

See [`docs/data-model.md`](docs/data-model.md) for the ER diagram and grain definition.

---

## Repository structure

```
broadband-adoption-bi/
├── data/                    # Star-schema CSVs (generated)
├── sql/                     # DDL + executive views
├── powerbi/
│   ├── dax/measures.dax     # KPI & trend measures
│   ├── power-query/         # M loader template
│   ├── theme/               # Executive dark JSON theme
│   └── report/              # Dashboard layout spec
├── scripts/
│   ├── generate_data.py
│   └── build_warehouse.py   # DuckDB validation
└── docs/
    └── dashboard-wireframe.md
```

---

## Quick start

```bash
git clone https://github.com/moeezislammalik/broadband-adoption-bi.git
cd broadband-adoption-bi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/generate_data.py      # Build CSVs
python scripts/build_warehouse.py    # Optional: DuckDB check
```

### Power BI Desktop

1. **Get Data** → Text/CSV → load all files in `data/`
2. Create relationships per `docs/data-model.md`
3. Import measures from `powerbi/dax/measures.dax`
4. Apply theme: **View** → **Themes** → **Browse** → `powerbi/theme/executive-dark.json`
5. Build pages per `powerbi/report/executive-dashboard-spec.md`

---

## Executive KPIs (DAX)

| Measure | Business use |
|---------|----------------|
| `Adoption Rate %` | Households with broadband / total households |
| `Penetration Rate %` | Service reach index for market depth |
| `Penetration Gap %` | Upsell / bundle opportunity |
| `Adoption YoY Change pp` | Trend monitoring for leadership |
| `Lift Ratio (NS:DG)` | Growth efficiency (new starts vs downgrades) |

---

## Dashboard pages

1. **State View** — ranked adoption by state (table + bar chart)
2. **Income Bracket** — adoption by income segment
3. **Urban vs Rural** — market-type comparison
4. **Technology Type** — fiber vs cable vs DSL vs FWA
5. **Trend Monitoring** — quarterly adoption & penetration lines

Wireframe: [`docs/dashboard-wireframe.md`](docs/dashboard-wireframe.md)

---

## Author

**Moeez Islam Malik** — Business Analyst · DePauw '26

- [Portfolio](https://moeezmalik.com)
- [LinkedIn](https://www.linkedin.com/in/moeez-malik/)
- [GitHub](https://github.com/moeezislammalik)

---

## License

MIT — see [LICENSE](LICENSE).
