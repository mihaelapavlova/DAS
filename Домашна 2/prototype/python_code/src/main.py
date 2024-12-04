import asyncio
import time
from scraper import get_stock_codes, scrape_all_stock_codes
from data_handler import load_data, save_data

async def main():
    start_time = time.time()
    stock_codes = get_stock_codes()
    print(f"Бројот на издавачи е: {len(stock_codes)}")

    existing_df = load_data()
    new_data = await scrape_all_stock_codes(stock_codes)

    if new_data:
        save_data(new_data, existing_df)

    end_time = time.time()
    duration = end_time - start_time
    minutes = duration / 60
    print(f"Преземањето на податоци трае: {minutes:.2f} минути.")

asyncio.run(main())
