import pandas as pd

def extract_max_kyc_activity(df: pd.DataFrame, col_index: int) -> pd.DataFrame:
    # Get the column name from the index
    col_name = df.columns[col_index]

    # Lists to store extracted results
    max_sections = []
    max_percentages = []

    for row in df.iloc[:, col_index]:
        try:
            if isinstance(row, list) and len(row) > 0:
                max_entry = max(row, key=lambda x: x.get('kycActivityPercentage', 0))
                max_sections.append(max_entry.get('kycSection', None))
                max_percentages.append(max_entry.get('kycActivityPercentage', None))
            else:
                max_sections.append(None)
                max_percentages.append(None)
        except Exception:
            max_sections.append(None)
            max_percentages.append(None)

    # Append new columns to the DataFrame
    df['maxKycSection'] = max_sections
    df['maxKycActivityPercentage'] = max_percentages

    return df
