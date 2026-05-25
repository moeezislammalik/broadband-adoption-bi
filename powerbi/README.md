# Power BI suite

## Contents

| Asset | Purpose |
|-------|---------|
| [`dax/measures.dax`](dax/measures.dax) | Executive KPI & trend measures |
| [`power-query/load_star_schema.m`](power-query/load_star_schema.m) | M template for CSV load |
| [`report/executive-dashboard-spec.md`](report/executive-dashboard-spec.md) | Page layout, theme, slicers, bookmarks |

## Quick import

1. Clone repo and run `python scripts/generate_data.py`
2. Open **Power BI Desktop** → Get data from `data/` CSVs
3. Model view → create relationships (see `docs/data-model.md`)
4. **Modeling** → New measure → paste from `measures.dax`
5. Build report per `report/executive-dashboard-spec.md`

## Semantic model name

`Broadband_Adoption_Executive`

## Privacy

Sample data and provider names are **fully synthetic**. No real operator or employer branding is used.
