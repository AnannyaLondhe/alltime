import json
import pandas as pd
import cx_Oracle
from datetime import datetime
from Cyberark_password_retrieval import retrieve_password

# ---------- Load Configs ----------
with open('db_config.json') as f:
    db_config = json.load(f)

with open('Queries.json') as f:
    queries_json = json.load(f)

# ---------- Helper: DB Connection ----------
def get_connection(db_key):
    cfg = db_config[db_key]
    password = retrieve_password(db_key)

    dsn = cx_Oracle.makedsn(
        cfg['hostname'],
        cfg['port'],
        service_name=cfg['service_name']
    )

    return cx_Oracle.connect(
        user=cfg['username'],
        password=password,
        dsn=dsn
    )

# ---------- Execution ----------
def run_queries_for_all_sources():
    month_year = datetime.now().strftime("%b_%Y")
    final_df = pd.DataFrame()

    for bu in queries_json['BU_BL_Mappings']:
        for key in bu:
            sources = bu[key]['Sources']

            for src in sources:
                source_name = src['Source_Name']
                sql = src['Query']['SQL']

                # Assume db key same as source or map if needed
                conn = get_connection(source_name)

                print(f"Running for {source_name}")
                df = pd.read_sql(sql, conn)
                conn.close()

                final_df = pd.concat([final_df, df], ignore_index=True)

    parquet_name = f"risk_assessment_{month_year}.parquet"
    final_df.to_parquet(parquet_name, index=False)
    print(f"Saved: {parquet_name}")

if __name__ == "__main__":
    run_queries_for_all_sources()
