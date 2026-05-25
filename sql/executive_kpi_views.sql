-- Executive KPI views for Power BI import or direct reporting

CREATE OR REPLACE VIEW vw_executive_kpi AS
SELECT
    d.year_quarter,
    d.is_current_quarter,
    s.state_name,
    s.region,
    seg.segment_name,
    seg.income_bracket,
    t.technology_name,
    p.provider_name,
    SUM(f.households_total) AS households_total,
    SUM(f.households_adopted) AS households_adopted,
    ROUND(100.0 * SUM(f.households_adopted) / NULLIF(SUM(f.households_total), 0), 2) AS adoption_rate_pct,
    ROUND(100.0 * AVG(f.penetration_rate), 2) AS penetration_rate_pct,
    ROUND(100.0 * AVG(f.penetration_gap), 2) AS penetration_gap_pct,
    ROUND(AVG(f.avg_mrc_usd), 2) AS avg_mrc_usd,
    SUM(f.new_starts) AS new_starts,
    SUM(f.downgrades) AS downgrades,
    ROUND(
        CAST(SUM(f.new_starts) AS DOUBLE) / NULLIF(SUM(f.downgrades), 0),
        2
    ) AS lift_ratio
FROM fact_broadband_adoption f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_state s ON f.state_key = s.state_key
JOIN dim_segment seg ON f.segment_key = seg.segment_key
JOIN dim_technology t ON f.technology_key = t.technology_key
JOIN dim_provider p ON f.provider_key = p.provider_key
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8;

-- YoY adoption trend by state (executive trend monitoring)
CREATE OR REPLACE VIEW vw_adoption_trend_yoy AS
SELECT
    s.state_name,
    d.year,
    ROUND(100.0 * SUM(f.households_adopted) / NULLIF(SUM(f.households_total), 0), 2) AS adoption_rate_pct,
    ROUND(100.0 * AVG(f.penetration_rate), 2) AS penetration_rate_pct
FROM fact_broadband_adoption f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_state s ON f.state_key = s.state_key
WHERE d.quarter = 1
GROUP BY s.state_name, d.year
ORDER BY s.state_name, d.year;
