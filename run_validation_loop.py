import os
import subprocess
from datetime import datetime, timedelta

# Define the date range
start_date = datetime.strptime("01-JAN-2025", "%d-%b-%Y")
end_date = datetime.strptime("31-MAR-2025", "%d-%b-%Y")

# Your Autosys job name
autosys_job = "AMLTEN_JOB_01"

# Full path to your data validation script
script_path = "/apps/infocaml/AMLTEN/scripts/python/amlten_check_data_validation.py"

# Loop over each day
while start_date <= end_date:
    date_str = start_date.strftime("%d-%b-%Y")
    
    print(f"\nRunning validation for date: {date_str}")
    
    # Construct the command to call the validation script
    cmd = ["python3", script_path, autosys_job, date_str, date_str]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Validation failed for {date_str}: {e}")
    
    # Move to next day
    start_date += timedelta(days=1)
