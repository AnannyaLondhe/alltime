import sys

if __name__ == '__main__':
    # Read command-line arguments
    args = sys.argv[1:]

    if len(args) < 2:
        print("Usage: python amlten_check_data_validation.py <FROM_DATE> <TO_DATE>")
        print("Example: python amlten_check_data_validation.py '01-JAN-2025' '31-MAR-2025'")
        sys.exit(1)

    # Hardcoded Autosys Job Name
    autosys_job = 'AML_JOB'  # You can change this to your default job name

    from_date_str = args[0].upper()
    to_date_str = args[1].upper()

    lg.step_name = "RUN FN_AML_CHECK_DATA_VALIDATION function"
    lg.start_step()

    try:
        lg.rc = FN_AML_CHECK_DATA_VALIDATION(autosys_job, from_date_str, to_date_str)
    except Exception as e:
        lg.dfnLogSTDout(f"[FATAL ERROR] {str(e)}")
        lg.rc = 1  # Non-zero return code for failure

    lg.end_step()
    lg.end_script()
