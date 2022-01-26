import yfinance as yf
import pandas as pd
import requests_cache

# Source: https://github.com/ranaroussi/yfinance
session = requests_cache.CachedSession('yfinance.cache', expire_after=3600)  # 3600 seconds = 1 hour
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'

def ticker(ticker_):
    return yf.Ticker(ticker_, session=session)

def history(ticker_, period):
    info = ticker(ticker_)
    return info.history(period=period)

def avg_daily_volume(ticker_, period):
    history_data = history(ticker_, period)
    total_volume_over_period, period_len = history_data['Volume'].sum(), len(history_data.index)
    return total_volume_over_period / period_len

def volume_change(ticker_, period):
    history_data = history(ticker_, period)
    curr_volume = history_data['Volume'].tail(1).iloc[0]
    return curr_volume / avg_daily_volume(ticker_, period)
    
def price_change(ticker_, period):
    history_data = history(ticker_, period)
    old_price, new_price = history_data['Close'].head(1).iloc[0], history_data['Close'].tail(1).iloc[0]
    return (new_price - old_price) / old_price

def price_momentum(ticker_, period):
    """
    From: https://www.investopedia.com/articles/technical/081501.asp
    """
    history_data = history(ticker_, period)

    dates = history_data.index.values
    curr_date, old_date = dates[-1], dates[0]
    delta_in_days = (curr_date - old_date).astype('timedelta64[D]').astype(int)

    new_price = history_data['Close'].tail(1).iloc[0]
    return new_price - (new_price * delta_in_days) # Kind of bad, maybe implementation wrong? 
