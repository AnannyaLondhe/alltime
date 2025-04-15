elif v_db_schema == 'AML':
    sql_as_of_dt = (f"""
        SELECT date_value 
        FROM aml.t_aml_application_date 
        WHERE date_id = '{v_date_id}' 
        AND date_value BETWEEN TO_DATE('{from_date_str}', 'DD-MON-YYYY') 
                          AND TO_DATE('{to_date_str}', 'DD-MON-YYYY') 
        ORDER BY date_value
    """)
    
    cur.execute(sql_as_of_dt)
    v_as_of_dt_rows = cur.fetchall()
    v_as_of_dt_list = [row[0].strftime('%d-%b-%Y') for row in v_as_of_dt_rows]

    return v_as_of_dt_list
