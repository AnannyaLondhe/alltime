received = []
monitored = []

# Case 1: Proper structure (US-style)
if isinstance(db_data.get('Data'), dict):
    received = db_data['Data'].get('Received', [])
    monitored = db_data['Data'].get('Monitored', [])

# Case 2: Flattened structure (CA-style already expanded)
elif 'Received' in db_data and 'Monitored' in db_data:
    received = db_data.get('Received', [])
    monitored = db_data.get('Monitored', [])

else:
    print(f"⚠️ Invalid data format for {db_key}")
    continue
