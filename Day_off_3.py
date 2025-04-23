def is_non_working_day(v_as_of_dt, etl_tenant):
    try:
        dt_obj = datetime.strptime(v_as_of_dt, '%d-%b-%Y')
        is_weekend = dt_obj.weekday() >= 5
        is_holiday = False

        v_count = cur.var(int)

        if etl_tenant.upper() == 'US':
            plsql_block = """
                DECLARE
                    v_count NUMBER;
                BEGIN
                    SELECT COUNT(*) INTO v_count 
                    FROM DWADMIN.V_SOURCE_DAY_OFF 
                    WHERE appl_cd = 'AT2' AND day_off = :as_of_dt;
                    :result := v_count;
                END;
            """
            cur.execute(plsql_block, as_of_dt=v_as_of_dt, result=v_count)

        elif etl_tenant.upper() == 'CA':
            plsql_block = """
                DECLARE
                    v_count NUMBER;
                BEGIN
                    SELECT COUNT(*) INTO v_count 
                    FROM AMLCA.INFOCCA_TA004 
                    WHERE A0020 = 5 AND A0370 = :as_of_dt;
                    :result := v_count;
                END;
            """
            cur.execute(plsql_block, as_of_dt=v_as_of_dt, result=v_count)

        if v_count.getvalue() > 0:
            is_holiday = True

        return is_weekend or is_holiday

    except Exception as e:
        lg.dfnLogSTDout(f"Error checking non-working day for {v_as_of_dt}: {str(e)}")
        return False
