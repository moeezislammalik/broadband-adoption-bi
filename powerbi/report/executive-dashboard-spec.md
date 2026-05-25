# Executive Dashboard — Report Specification

De-identified **Broadband Adoption Executive Portal** layout inspired by a professional telecom BI template. No company branding is included.

## Theme

| Element | Value |
|---------|--------|
| Background | `#1B2838` (charcoal navy) |
| Card background | `#243447` |
| Primary accent | `#3B82F6` (executive blue) |
| Text | `#F8FAFC` / `#94A3B8` |
| Font | Segoe UI (Power BI default) |

## Page layout (16:9)

### Left panel — Filters (slicers)

Vertical stack, dropdown style:

1. **State** — `dim_state[state_name]` (24 states)
2. **Region** — `dim_state[region]`
3. **Income Bracket** — `dim_segment[income_bracket]`
4. **Market Type** — `dim_segment[market_type]` (Urban / Suburban / Rural)
5. **Technology** — `dim_technology[technology_name]`
6. **Provider** — `dim_provider[provider_name]`
7. **Year** — `dim_date[year]`
8. **Quarter** — `dim_date[year_quarter]`

Header block:

- Title: **Broadband Adoption Executive Portal**
- Subtitle: `Report Subtitle` measure
- As-of date: `SELECTEDVALUE(dim_date[month_name])`

### Top row — KPI cards

| Card | Measure | Format |
|------|---------|--------|
| Adoption Rate | `[Adoption Rate %]` | 0.0% |
| Penetration Rate | `[Penetration Rate %]` | 0.0% |
| Penetration Gap | `[Penetration Gap %]` | 0.0% |
| Adoption YoY | `[Adoption YoY Change pp]` | +0.0 pp; subtitle `[Adoption Trend Arrow]` |

Optional secondary row (operations):

| New Starts | Downgrades | Lift Ratio | Avg MRC |
|------------|------------|------------|---------|
| `[New Starts]` | `[Downgrades]` | `[Lift Ratio Label]` | `[Avg MRC USD]` |

### Center — Tab navigator

Buttons (bookmark pages):

1. **State View** (default)
2. **Income Bracket**
3. **Urban vs Rural**
4. **Technology Type**
5. **Trend Monitoring**

### State View page

- **Table (left):** `state_name`, `[Adoption Rate %]`, `[Penetration Rate %]`, `[Penetration Gap %]`
- **Bar chart (right):** Horizontal bars, `state_name` vs `[Adoption Rate %]`, sorted descending
- **Title:** Count of Households by State — Adoption Rate %

### Trend Monitoring page

- **Line chart:** `dim_date[year_quarter]` × `[Adoption Rate %]` and `[Penetration Rate %]`
- **Clustered column:** YoY by `dim_date[year]` — `[Adoption YoY Change pp]`

### Income Bracket / Urban vs Rural / Technology pages

- Matrix: Segment or Technology × State with `[Adoption Rate %]`
- Small multiples optional for executive pack

## Relationships (star schema)

```
dim_date[date_key] ──► fact_broadband_adoption[date_key]
dim_state[state_key] ──► fact_broadband_adoption[state_key]
dim_segment[segment_key] ──► fact_broadband_adoption[segment_key]
dim_technology[technology_key] ──► fact_broadband_adoption[technology_key]
dim_provider[provider_key] ──► fact_broadband_adoption[provider_key]
```

All dimensions: **single direction**, one-to-many to fact.

## Build steps in Power BI Desktop

1. Get Data → Text/CSV → load all `data/*.csv` files
2. Create relationships per diagram in `docs/data-model.md`
3. Paste measures from `powerbi/dax/measures.dax`
4. Apply theme JSON (optional) or format manually per theme table above
5. Create bookmarks for each tab page
6. Publish to Power BI Service → Executive workspace (optional)
