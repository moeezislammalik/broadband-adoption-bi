# Broadband Adoption Executive BI

**March 2026** · Star-schema · 24 states · Executive dashboard

**[Project Link](https://github.com/moeezislammalik/broadband-adoption-bi)**

---

## Executive dashboard (PDF)

**Due to privacy reasons**, the live **Power BI (`.pbix`) file is not included** in this repository. The executive dashboard is published as a **PDF** instead.

### [Download Executive Dashboard PDF](docs/executive-dashboard.pdf)

The PDF replicates the **exact executive BI layout** (blue sidebar, 4 KPI cards, 8 slicers, tab bar, Mgmt Area table + horizontal bar chart). Company branding is **NeatFiber X Business Intelligence** (de-identified — not the original operator).

Includes:

- **New Starts**, **Downgrades**, **Lift Ratio (NS:DG)**, **Avg MRC** KPI scorecards  
- **Mgmt Area** / **HSD Balance** table with **Count of SingleviewAccount by Mgmt Area** bar chart  
- Same slicer and tab names as the reference telecom executive template  
- **Due to privacy reasons**, no `.pbix` file is published

See [`docs/PRIVACY.md`](docs/PRIVACY.md) for the full privacy policy.

---

## Portfolio summary

- Designed a **star-schema** warehouse (`dim_*` + `fact_broadband_adoption`) for multi-state broadband KPIs  
- Built **executive views** for adoption rate, penetration, gap analysis, and trend monitoring  
- Delivered **PDF executive dashboard** plus SQL, DAX reference, and data model documentation  

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

See [`docs/data-model.md`](docs/data-model.md) for the ER diagram.

---

## Repository structure

```
broadband-adoption-bi/
├── docs/
│   ├── executive-dashboard.pdf   ← Portfolio deliverable (not .pbix)
│   └── PRIVACY.md
├── data/                         # Star-schema CSVs
├── sql/                          # DDL + executive views
├── powerbi/                      # DAX/M reference only (no .pbix)
└── scripts/
    ├── generate_data.py
    ├── build_warehouse.py
    └── generate_dashboard_pdf.py
```

---

## Quick start

```bash
git clone https://github.com/moeezislammalik/broadband-adoption-bi.git
cd broadband-adoption-bi
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/generate_data.py
python scripts/build_warehouse.py
python scripts/generate_dashboard_pdf.py   # → docs/executive-dashboard.pdf
```

---

## Power BI reference (not distributed)

The `powerbi/` folder contains **DAX measures**, **Power Query templates**, and a **layout specification** for analysts who want to rebuild the model locally.  

**No `.pbix` file is published — due to privacy reasons.** Use the PDF above for portfolio and recruiter review.

---

## Author

**Moeez Islam Malik** — Business Analyst · DePauw '26

- [Portfolio](https://moeezmalik.com)
- [LinkedIn](https://www.linkedin.com/in/moeez-malik/)
- [GitHub](https://github.com/moeezislammalik)

---

## License

MIT — see [LICENSE](LICENSE).
