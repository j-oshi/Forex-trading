import pandas as pd
import aiohttp
import asyncio
import nest_asyncio
import requests
from bs4 import BeautifulSoup as bs
import os, sys

parent_dir = os.path.abspath('..')
forex_file = parent_dir + '\datas\currencies.csv'

nest_asyncio.apply()

def get_all_currencies():
    """dataframe of info of all currency code in the world"""
    try:

        url = 'https://taxsummaries.pwc.com/glossary/currency-codes'
        request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(request.text, "lxml")        
        table = soup.find('table')  
        tr = table.find_all("tr")
        if(tr is not None):
            header = []
            for td in tr[:1]:
                header_column = td.findAll('td')
                header_row = []
                for title in header_column:
                    header_row.append(title.text)
                header.append(header_row)

            body = []
            for table_row in tr[1:]:
                columns = table_row.findAll('td')
                output_row = []
                for column in columns:
                    output_row.append(column.text)
                body.append(output_row)
                        
            dataFrame = pd.DataFrame(data = body, columns = header)        

            # Converting Pandas DataFrame
            # into CSV file
            dataFrame.to_csv(forex_file, index=False)
            print('Currencies list download complete')
    except requests.exceptions.Timeout:
      print("Timeout occurred")

async def getExchangeRateFor(symbol):
        """Get all exchange for currency"""
        url = f'https://finance.yahoo.com/lookup?s={symbol}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    r = await response.text()
                    soup = bs(r, "lxml")

                    currency = {}
                    currency['symbol'] = symbol
                    table = soup.find('table', class_='lookup-table') 
                    if table is None:
                        currency['price'] = ''
                        return currency
                    else:
                        row = table.find_all("tr")
                        exchange_rate = []
                        for td in row[1:2]:
                            currency_row = td.findAll('td')
                            exchange_row = []
                            for item in currency_row:
                                exchange_row.append(item.text)
                            exchange_rate.append(exchange_row)
                        if len(exchange_rate[0]) > 2:
                            currency['price'] = exchange_rate[0][2]
                        else:
                            currency['price'] = ''
                        return currency

        except requests.exceptions.Timeout:
            print("Timeout occurred")

def getYahooAllExchangeRateFor(symbols):
    loop = asyncio.get_event_loop()
    coroutines = [getExchangeRateFor(symbol) for symbol in symbols]
    L = asyncio.gather(*coroutines)
    results = loop.run_until_complete(L)
    return results

async def getDetailExchangeRateFor(symbol):
        """Get all exchange for currency"""
        url = f'https://finance.yahoo.com/quote/{symbol}%3DX?p={symbol}%3DX'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    r = await response.text()
                    soup = bs(r, "lxml")

                    currency = {}
                    currency['symbol'] = symbol
                    marketPrice = soup.find_all(attrs={"data-test": "qsp-price"})
                    currency['regularMarketPrice'] = marketPrice[0].text if len(marketPrice) > 0 else ""

                    marketChange = soup.find_all(attrs={"data-test": "qsp-price-change"})
                    currency['regularMarketChange'] = marketChange[0].text if len(marketChange) > 0 else ""

                    marketChangePercent = soup.find_all("fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)")
                    currency['regularMarketChangePercent'] = marketChangePercent[1].text if len(marketChangePercent) > 1 else ""

                    leftSummaryTable = soup.find_all(attrs={"data-test": "left-summary-table"})
                    if leftSummaryTable is None:
                        currency['previous_close'] = ''
                        currency['open'] = ''
                        currency['bid'] = ''
                    else:
                        if len(leftSummaryTable) > 0:
                            row = leftSummaryTable[0].findAll("tr")
                            currency_value = [[td for td in tr] for tr in row]
                            currency['previous_close'] = currency_value[0][1].text
                            currency['open'] = currency_value[1][1].text
                            currency['bid'] = currency_value[2][1].text

                    rightSummaryTable = soup.find_all(attrs={"data-test": "right-summary-table"})
                    if rightSummaryTable is None:
                        currency['day_range'] = ''
                        currency['year_Week_range'] = ''
                        currency['ask'] = ''
                    else:
                        if len(rightSummaryTable) > 0:
                            row = rightSummaryTable[0].findAll("tr")
                            currency_value = [[td for td in tr] for tr in row]
                            currency['day_range'] = currency_value[0][1].text
                            currency['year_Week_range'] = currency_value[1][1].text
                            currency['ask'] = currency_value[2][1].text                       

                    return currency

        except requests.exceptions.Timeout:
            print("Timeout occurred")

def getYahooAllDetailExchangeRateFor(symbols):
    loop = asyncio.get_event_loop()
    coroutines = [getDetailExchangeRateFor(symbol) for symbol in symbols]
    L = asyncio.gather(*coroutines)
    results = loop.run_until_complete(L)
    return results
