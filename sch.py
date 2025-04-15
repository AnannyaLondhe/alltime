as_of_dates = fn_get_as_of_dt(autosys_schema, sql_main[i][2])

for v_as_of_dt in as_of_dates:
    # your existing logic here
    # e.g., skip weekend check
    v_weekend_check = sql_main[i][19]
    if is_weekend(v_as_of_dt) and v_weekend_check == 1:
        lg.dfnLogSTDout(f"Skipping validation for weekend date: {v_as_of_dt}")
        continue
    # ... and so on for rest of your logic
