import asyncio
from api.scraper_service import scrape_stock_code
from api.data_handler_service import save_data
import pandas as pd



async def main():
    stock_codes = ["AAPL", "GOOG"]
    start_date = "01.01.2015"
    end_date = "31.12.2025"

    new_data = await scrape_stock_code(stock_codes[0], start_date, end_date)

    if new_data:
        existing_df = pd.DataFrame()
        message = save_data(new_data, existing_df)
        print(message)

asyncio.run(main())