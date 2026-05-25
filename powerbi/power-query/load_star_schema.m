// Broadband Adoption — Power Query (M) loader
// Power BI Desktop: Home → Transform data → New Source → Blank Query → Advanced Editor

let
    RootPath = "C:\path\to\broadband-adoption-bi\data",  // update to your clone path

    LoadCsv = (tableName as text) =>
        let
            Source = Csv.Document(
                File.Contents(RootPath & "\" & tableName & ".csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
            ),
            Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
            Typed = Table.TransformColumnTypes(
                Promoted,
                List.Transform(
                    Table.ColumnNames(Promoted),
                    each {_, type text}
                )
            )
        in
            Promoted,

    dim_date = Table.TransformColumnTypes(
        LoadCsv("dim_date"),
        {
            {"date_key", Int64.Type},
            {"date", type date},
            {"year", Int64.Type},
            {"quarter", Int64.Type},
            {"is_current_quarter", type logical}
        }
    ),

    dim_state = LoadCsv("dim_state"),
    dim_segment = LoadCsv("dim_segment"),
    dim_technology = LoadCsv("dim_technology"),
    dim_provider = LoadCsv("dim_provider"),

    fact_broadband_adoption = Table.TransformColumnTypes(
        LoadCsv("fact_broadband_adoption"),
        {
            {"date_key", Int64.Type},
            {"households_total", Int64.Type},
            {"households_adopted", Int64.Type},
            {"adoption_rate", type number},
            {"penetration_rate", type number},
            {"penetration_gap", type number},
            {"avg_mrc_usd", type number},
            {"new_starts", Int64.Type},
            {"downgrades", Int64.Type}
        }
    )
in
    fact_broadband_adoption
