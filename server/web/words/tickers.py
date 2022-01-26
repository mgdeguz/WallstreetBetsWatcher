import requests
import pandas as pd
import requests_cache
import io

# Source: https://realpython.com/caching-external-api-requests/
requests_cache.install_cache('tickers', backend='sqlite', expire_after=86400) # Cache results for 86400 seconds = 24 hours

NASDAQ = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nasdaq"
NYSE = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nyse"

# Necessary otherwise NASDAQ will block our request
header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
}

def get_tickers():
    # Get NASDAQ data
    req_nasdaq = requests.get(url=NASDAQ, headers=header)
    req_nyse = requests.get(url=NYSE, headers=header)

    # Convert to data
    nasdaq_data = req_nasdaq.json()
    nyse_data = req_nyse.json()

    # Get stock names -- located in rows
    nasdaq_rows = nasdaq_data['data']['table']['rows']
    nyse_rows = nyse_data['data']['table']['rows']

    tickers = {row['symbol'] for row in nasdaq_rows} | {row['symbol'] for row in nyse_rows}

    return tickers

def remove_dollarsign(ticker):
    if ticker[0] == '$':
        return ticker[1:]
    return ticker

def format_ticker(ticker):
    return remove_dollarsign(ticker).upper()

TICKERS_UPPER = get_tickers()

TICKERS_LOWER = {ticker.lower() for ticker in TICKERS_UPPER}
TICKERS_CAPITALIZED = {ticker.capitalize() for ticker in TICKERS_LOWER} # ie: Tsla

TICKERS_DOLLAR_SIGNED = {'$' + ticker for ticker in TICKERS_UPPER} | {'$' + ticker.lower() for ticker in TICKERS_CAPITALIZED}

TICKERS = TICKERS_UPPER | TICKERS_CAPITALIZED | TICKERS_DOLLAR_SIGNED
