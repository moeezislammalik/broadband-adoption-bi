-- Broadband Adoption Executive BI — Star Schema (SQL Server / DuckDB compatible)
-- De-identified portfolio model · 24 states · March 2026

CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,
    date            DATE NOT NULL,
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL,
    year_quarter    VARCHAR(10) NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    is_current_quarter BOOLEAN NOT NULL
);

CREATE TABLE dim_state (
    state_key               VARCHAR(2) PRIMARY KEY,
    state_name              VARCHAR(50) NOT NULL,
    region                  VARCHAR(20) NOT NULL,
    population_k            INTEGER NOT NULL,
    target_penetration_pct  DECIMAL(5,1) NOT NULL
);

CREATE TABLE dim_segment (
    segment_key     VARCHAR(10) PRIMARY KEY,
    segment_name    VARCHAR(30) NOT NULL,
    market_type     VARCHAR(20) NOT NULL,
    income_bracket  VARCHAR(20) NOT NULL
);

CREATE TABLE dim_technology (
    technology_key   VARCHAR(10) PRIMARY KEY,
    technology_name  VARCHAR(30) NOT NULL,
    speed_tier       VARCHAR(20) NOT NULL
);

CREATE TABLE dim_provider (
    provider_key   VARCHAR(10) PRIMARY KEY,
    provider_name  VARCHAR(50) NOT NULL
);

CREATE TABLE fact_broadband_adoption (
    date_key            INTEGER NOT NULL REFERENCES dim_date(date_key),
    state_key           VARCHAR(2) NOT NULL REFERENCES dim_state(state_key),
    segment_key         VARCHAR(10) NOT NULL REFERENCES dim_segment(segment_key),
    technology_key      VARCHAR(10) NOT NULL REFERENCES dim_technology(technology_key),
    provider_key        VARCHAR(10) NOT NULL REFERENCES dim_provider(provider_key),
    households_total    INTEGER NOT NULL,
    households_adopted  INTEGER NOT NULL,
    adoption_rate       DECIMAL(8,4) NOT NULL,
    penetration_rate      DECIMAL(8,4) NOT NULL,
    penetration_gap       DECIMAL(8,4) NOT NULL,
    avg_mrc_usd           DECIMAL(8,2) NOT NULL,
    new_starts            INTEGER NOT NULL,
    downgrades            INTEGER NOT NULL,
    PRIMARY KEY (date_key, state_key, segment_key, technology_key, provider_key)
);
