if autosys_schema == 'AML':
    date_range = get_date_range(from_date_str, to_date_str)
else:
    date_range = fn_get_as_of_dt(autosys_schema, sql_main[i][2], from_date_str, to_date_str)
