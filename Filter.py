import pandas as pd
import re

# Load the Excel file
df = pd.read_excel('your_file.xlsx')  # Replace with your actual file name

# Replace 'YourColumnName' with your actual column name
def extract_text(text):
    if isinstance(text, str):
        match = re.search(r',\s*(.*?)\s*as FILTER', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None  # or return "" if you prefer empty string for no match

df['FILTER'] = df['YourColumnName'].apply(extract_text)

# Save the result (optional)
df.to_excel('output_with_filter.xlsx', index=False)

# Show result
print(df[['YourColumnName', 'FILTER']])
