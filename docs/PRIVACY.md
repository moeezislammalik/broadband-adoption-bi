# Privacy & deliverable policy

## Why there is no Power BI file (`.pbix` / `.pbip`)

**Due to privacy reasons**, the live Power BI Desktop report and semantic model tied to real employer systems are **not published** in this repository.

Publishing a `.pbix` file could expose:

- Internal data connection strings or gateway references  
- Proprietary report structure from a prior employer project  
- Branding, naming, or operational metadata that must stay confidential  

## What is published instead

| Deliverable | Location |
|-------------|----------|
| **Executive dashboard (PDF)** | [`executive-dashboard.pdf`](executive-dashboard.pdf) |
| Star-schema CSVs & SQL | `data/`, `sql/` |
| DAX / M reference (build-your-own) | `powerbi/` (documentation only) |
| Dashboard layout specification | `powerbi/report/executive-dashboard-spec.md` |

The PDF is the **portfolio-facing executive view** — a pixel-faithful replica of a professional telecom BI dashboard (de-identified as **NeatFiber X Business Intelligence**), including Mgmt Area analysis, HSD Balance, and standard lift/MRC KPIs.

## Data in this repo

All state, provider, and metric values are **synthetic** and generated for portfolio demonstration. No real company names are used.

## Regenerating the PDF

```bash
python scripts/generate_data.py
python scripts/build_warehouse.py
python scripts/generate_dashboard_pdf.py
```

Output: `docs/executive-dashboard.pdf`
