import pandas as pd
import json
import glob

# ---------- Load Mapping Parquets ----------
assessment_map = pd.read_parquet("Assessment_Unit_mapping.parquet")
assessment_map['metier_code'] = assessment_map['metier_code'].str.lower()

countries_df = pd.read_parquet("t_mon_countries.parquet")
countries_df['code'] = countries_df['code'].str.lower()

# ---------- Step 1: Join Assessment Unit ----------
def join_assessment_unit(month_file):
    df = pd.read_parquet(month_file)
    df['metier_code'] = df['metier_code'].str.lower()

    merged = df.merge(
        assessment_map[['metier_code', 'Assessment_Unit']],
        how='left',
        on='metier_code'
    )

    new_name = month_file.replace(".parquet", "_after_join.parquet")
    merged.to_parquet(new_name, index=False)
    return new_name

# ---------- Step 2: Join Country Sensitivity & MSC ----------
def join_country_details(file_name):
    df = pd.read_parquet(file_name)

    df['Country_of_Originator'] = df['Country_of_Originator'].str.lower()
    df['Country_of_Beneficiary'] = df['Country_of_Beneficiary'].str.lower()

    df = df.merge(
        countries_df,
        how='left',
        left_on='Country_of_Originator',
        right_on='code'
    )

    df = df.merge(
        countries_df,
        how='left',
        left_on='Country_of_Beneficiary',
        right_on='code',
        suffixes=('_orig', '_bene')
    )

    df.to_parquet(file_name, index=False)
    return df

# ---------- Step 3: Summarisation ----------
def summarise_all_months():
    files = glob.glob("risk_assessment_*_after_join.parquet")
    full_year_df = pd.concat([join_country_details(f) for f in files])

    summary = full_year_df.groupby(
        ['Assessment_Unit', 'Jurisdiction_Risk']
    ).agg(
        Volume_Incoming=('Direction_of_Payment',
                         lambda x: (x == 'Credit').sum()),
        Volume_Outgoing=('Direction_of_Payment',
                         lambda x: (x == 'Debit').sum()),
        Value_Incoming=('Amount_EUR',
                        lambda x: full_year_df.loc[x.index]
                        .query("Direction_of_Payment=='Credit'")['Amount_EUR'].sum()),
        Value_Outgoing=('Amount_EUR',
                        lambda x: full_year_df.loc[x.index]
                        .query("Direction_of_Payment=='Debit'")['Amount_EUR'].sum()),
        Number_of_Clients=('Client_ID', 'nunique'),
        Total_Volume=('Transaction_ID', 'count'),
        Total_Value=('Amount_EUR', 'sum')
    ).reset_index()

    summary.to_excel("Year_End_Risk_Summary.xlsx", index=False)
    print("Year End Summary Generated")

# ---------- Execute ----------
if __name__ == "__main__":
    month_files = glob.glob("risk_assessment_*.parquet")

    after_join_files = [join_assessment_unit(f) for f in month_files]
    summarise_all_months()
