import os
import sys
import subprocess
from datetime import datetime, timedelta

if len(sys.argv) < 4:
    print("Usage: python3 run_validation_loop.py <AUTOSYS_JOB> <START_DATE> <END_DATE>")
    print("Example: python3 run_validation_loop.py AMLTEN_JOB_01 01-JAN-2025 31-MAR-2025")
    sys.exit(1)

autosys_job = sys.argv[1]
start_date_str = sys.argv[2]
end_date_str = sys.argv[3]

try:
    start_date = datetime.strptime(start_date_str, "%d-%b-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%b-%Y")
except ValueError:
    print("Dates must be in DD-MMM-YYYY format. Example: 01-JAN-2025")
    sys.exit(1)

script_path = "/apps/infocaml/AMLTEN/scripts/python/amlten_check_data_validation.py"

while start_date <= end_date:
    date_str = start_date.strftime("%d-%b-%Y")
    
    print(f"\nRunning validation for date: {date_str}")
    
    cmd = ["python3", script_path, autosys_job, date_str, date_str]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Validation failed for {date_str}: {e}")
    
    start_date += timedelta(days=1)
