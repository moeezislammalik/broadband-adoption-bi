# Star-schema data model

**Broadband Adoption Executive BI** · 24 states · March 2026

## Architecture

```mermaid
erDiagram
    dim_date ||--o{ fact_broadband_adoption : date_key
    dim_state ||--o{ fact_broadband_adoption : state_key
    dim_segment ||--o{ fact_broadband_adoption : segment_key
    dim_technology ||--o{ fact_broadband_adoption : technology_key
    dim_provider ||--o{ fact_broadband_adoption : provider_key

    dim_date {
        int date_key PK
        date date
        int year
        int quarter
        string year_quarter
    }

    dim_state {
        string state_key PK
        string state_name
        string region
        int population_k
        decimal target_penetration_pct
    }

    dim_segment {
        string segment_key PK
        string segment_name
        string market_type
        string income_bracket
    }

    dim_technology {
        string technology_key PK
        string technology_name
        string speed_tier
    }

    dim_provider {
        string provider_key PK
        string provider_name
    }

    fact_broadband_adoption {
        int date_key FK
        string state_key FK
        string segment_key FK
        string technology_key FK
        string provider_key FK
        int households_total
        int households_adopted
        decimal adoption_rate
        decimal penetration_rate
        decimal penetration_gap
        decimal avg_mrc_usd
        int new_starts
        int downgrades
    }
```

## Design principles

| Principle | Implementation |
|-----------|----------------|
| **Star schema** | Single fact table; conformed dimensions; no snowflaking |
| **Grain** | One row per state × segment × technology × provider × month |
| **Additive facts** | Households, new starts, downgrades |
| **Semi-additive** | Adoption/penetration rates — use measures, not SUM in visuals |
| **Role-playing** | `dim_date` supports YoY via `SAMEPERIODLASTYEAR` |

## Executive metrics

| Metric | Definition |
|--------|------------|
| **Adoption rate** | Adopted households ÷ total households |
| **Penetration** | Service reach beyond base adoption (basket uplift) |
| **Penetration gap** | Penetration − adoption (upsell / bundle opportunity) |
| **YoY trend** | Current quarter vs prior year same quarter |

## Data volume

- **States:** 24
- **Months:** 39 (Jan 2023 – Mar 2026)
- **Fact rows:** ~150K+ (sparse cross-product of dimensions)

Regenerate: `python scripts/generate_data.py`
