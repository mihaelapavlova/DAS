from datetime import datetime, timedelta

end_date = datetime.now().strftime("%d.%m.%Y")
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime("%d.%m.%Y")
historical_records_file = 'mse_historical_data.csv'
