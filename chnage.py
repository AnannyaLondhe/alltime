def summarise_all_months():
    fetch_country_reference()
    countries_df = pd.read_parquet("t_mon_countries.parquet")

    month_files = glob.glob("risk_assessment_*.parquet")
    after_join_files = [join_assessment_unit(f) for f in month_files]

    full_year_df = pd.concat([
        join_country_details(f, countries_df)
        for f in after_join_files
    ], ignore_index=True)

    # ---------------- Incoming (Credit → Originator Risk) ----------------
    incoming_df = full_year_df[
        full_year_df['Direction_of_Payment'].str.upper() == 'CREDIT'
    ].copy()

    incoming_summary = (
        incoming_df
        .groupby(['Assessment_Unit', 'Jurisdiction_Risk_orig'])
        .agg(
            Volume_Incoming=('Transaction_ID', 'count'),
            Value_Incoming=('Amount_EUR', 'sum')
        )
        .reset_index()
        .rename(columns={'Jurisdiction_Risk_orig': 'Jurisdiction_Risk'})
    )

    # ---------------- Outgoing (Debit → Beneficiary Risk) ----------------
    outgoing_df = full_year_df[
        full_year_df['Direction_of_Payment'].str.upper() == 'DEBIT'
    ].copy()

    outgoing_summary = (
        outgoing_df
        .groupby(['Assessment_Unit', 'Jurisdiction_Risk_bene'])
        .agg(
            Volume_Outgoing=('Transaction_ID', 'count'),
            Value_Outgoing=('Amount_EUR', 'sum')
        )
        .reset_index()
        .rename(columns={'Jurisdiction_Risk_bene': 'Jurisdiction_Risk'})
    )

    # ---------------- Merge both ----------------
    summary = pd.merge(
        incoming_summary,
        outgoing_summary,
        on=['Assessment_Unit', 'Jurisdiction_Risk'],
        how='outer'
    ).fillna(0)

    # ---------------- Totals ----------------
    summary['Total_Volume'] = (
        summary['Volume_Incoming'] + summary['Volume_Outgoing']
    )

    summary['Total_Value'] = (
        summary['Value_Incoming'] + summary['Value_Outgoing']
    )

    summary = summary.sort_values(
        ['Assessment_Unit', 'Jurisdiction_Risk']
    )

    summary.to_excel("Year_End_Risk_Summary.xlsx", index=False)
    print("Year End Summary Generated")
