import json
import pandas as pd
import oracledb
from datetime import datetime
from Cyberark_password_retrieval import retrieve_password

# ---------- Load Configs ----------
with open('db_config.json') as f:
    db_config = json.load(f)

with open('Queries.json') as f:
    queries_json = json.load(f)

# ---------- Oracle Connection using oracledb ----------
def get_connection(db_key):
    cfg = db_config[db_key]
    password = retrieve_password(db_key)

    dsn = f"{cfg['hostname']}:{cfg['port']}/{cfg['service_name']}"

    conn = oracledb.connect(
        user=cfg['username'],
        password=password,
        dsn=dsn
    )
    return conn

# ---------- Extract Sources Properly ----------
def extract_sources(sources_list):
    # First dict contains Name_of_Sources
    name_block = sources_list[0]
    source_names = name_block['Name_of_Sources']

    source_queries = {}

    for item in sources_list[1:]:
        if 'Source_Name' in item and item['Source_Name'] in source_names:
            source_queries[item['Source_Name']] = {
                'db_key': item['DB_key'],
                'sql': item['Query']['SQL']
            }

    return source_queries

# ---------- Main Execution ----------
def run_monthly_extraction():
    month_year = datetime.now().strftime("%b_%Y")
    final_df = pd.DataFrame()

    for bu in queries_json['BU_BL_Mappings']:
        for key in bu:
            sources_list = bu[key]['Sources']

            sources = extract_sources(sources_list)

            for src_name, details in sources.items():
                print(f"Running query for {src_name}")

                conn = get_connection(details['db_key'])
                df = pd.read_sql(details['sql'], conn)
                conn.close()

                final_df = pd.concat([final_df, df], ignore_index=True)

    parquet_name = f"risk_assessment_{month_year}.parquet"
    final_df.to_parquet(parquet_name, index=False)
    print(f"Saved {parquet_name}")

# ---------- Execute ----------
if __name__ == "__main__":
    run_monthly_extraction()
