import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_data(stock_code, from_date, to_date):
    url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    payload = {"FromDate": from_date, "ToDate": to_date, "Code": stock_code}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                table = soup.find('table', {'id': 'resultsTable'})
                if table:
                    return [[stock_code] + [col.text.strip() for col in row.find_all('td')]
                            for row in table.find_all('tr')[1:]]
            return []

async def scrape_stock_code(stock_code, start_date, end_date):
    data = []
    for from_date, to_date in date_ranges(start_date, end_date, days=730):
        result = await fetch_data(stock_code, from_date, to_date)
        data.extend(result)
    return data