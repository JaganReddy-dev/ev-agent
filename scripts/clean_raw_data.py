from ev_agent.db import get_connection

with get_connection() as con:
    con.execute("""
        CREATE OR REPLACE TABLE ev_silver AS
        SELECT
            vin_110                                          AS vin_prefix,
            county,
            city,
            state,
            CAST(postal_code AS VARCHAR)                     AS postal_code,   -- ID,
            model_year,
            make,
            model,
            electric_vehicle_type,
            clean_alternative_fuel_vehicle_cafv_eligibility  AS cafv_eligibility,
            NULLIF(electric_range, 0)                        AS electric_range, -- 0 = not researched
            legislative_district,
            dol_vehicle_id,
            vehicle_location,
            electric_utility,
            CAST(_2020_geoid AS VARCHAR)                     AS census_tract    -- ID, not a number
        FROM ev_raw
    """)
    n = con.execute("SELECT COUNT(*) FROM ev_silver").fetchone()
    if n is None:
        raise RuntimeError("COUNT(*) query returned no result")
    print(f"Built ev_silver: {n[0]} rows")
