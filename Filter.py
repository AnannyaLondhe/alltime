import pandas as pd

# Load the Excel file
df = pd.read_excel('your_file.xlsx')  # Replace with your actual file name

# Replace 'YourColumnName' with the actual column name you want to process
def extract_between_commas(text):
    if isinstance(text, str):
        parts = text.split(',')
        if len(parts) >= 3:
            return parts[1].strip()  # Text between first and second comma
    return None  # or return text / "" if you want to keep original/empty

df['FILTER'] = df['YourColumnName'].apply(extract_between_commas)

# Save to a new Excel file (optional)
df.to_excel('output_with_filter.xlsx', index=False)

print(df[['YourColumnName', 'FILTER']])
