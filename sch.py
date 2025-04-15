def get_date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%d-%b-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%b-%Y")
    date_list = []

    while start_date <= end_date:
        date_list.append(start_date.strftime('%d-%b-%Y'))
        start_date += timedelta(days=1)
    
    return date_list
