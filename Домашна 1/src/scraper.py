import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import start_date, end_date
import requests

def get_stock_codes():
    url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    response = requests.get(url)
    rawHtml = response.text
    soup = BeautifulSoup(rawHtml, "html.parser")
    dropdown = soup.find("select", {"name": "Code"})
    stock_codes = [option['value'] for option in dropdown.find_all("option") if not any(char.isdigit() for char in option['value'])]
    return stock_codes

async def fetch_data(session, stock_code, from_date, to_date):
    url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    payload = {"FromDate": from_date, "ToDate": to_date, "Code": stock_code}
    async with session.post(url, data=payload) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find('table', {'id': 'resultsTable'})
            if table:
                return [[stock_code] + [col.text.strip() for col in row.find_all('td')]
                        for row in table.find_all('tr')[1:]]
        return []

async def scrape_stock_code(session, stock_code, start_date, end_date):
    data = []
    for from_date, to_date in date_ranges(start_date, end_date, days=730):
        result = await fetch_data(session, stock_code, from_date, to_date)
        data.extend(result)
    return data

async def scrape_all_stock_codes(stock_codes):
    all_data = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_stock_code(session, stock_code, start_date, end_date) for stock_code in stock_codes]
        all_results = await asyncio.gather(*tasks)
        for result in all_results:
            all_data.extend(result)
    return all_data

def date_ranges(start_date, end_date, days=730):
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(end_date, "%d.%m.%Y")
    while start < end:
        next_end = min(start + timedelta(days=days), end)
        yield start.strftime("%d.%m.%Y"), next_end.strftime("%d.%m.%Y")
        start = next_end + timedelta(days=1)
