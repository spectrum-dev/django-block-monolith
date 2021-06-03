import pandas as pd

from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.fundamentaldata import FundamentalData

from blocks.settings import env

# from app import settings

def get_crypto_data(symbol, data_type='intraday', start_date=None, end_date=None):
    # TODO: Swap out with AlphaVantage Key
    crypto = CryptoCurrencies(key=env("ALPHA_VANTAGE_API_KEY"), output_format='pandas')
    data, meta_data = None, None
    if (data_type == "daily"):
        data, meta_data = crypto.get_digital_currency_daily(symbol=symbol, market='USD')
    elif (data_type == "weekly"):
        data, meta_data = crypto.get_digital_currency_weekly(symbol=symbol, market='USD')
    elif (data_type == "monthly"):
        data, meta_data = crypto.get_digital_currency_monthly(symbol=symbol, market='USD')
    else:
        raise f"Data Type: {data_type}"

    # Renames columns from defalt provided by AlphaVantage to more standard terms
    data = data.rename(columns={
        '1a. open (USD)': 'open(USD)',
        '1b. open (USD)': 'open(USD)',
        '2a. high (USD)': 'high(USD)',
        '2b. high (USD)': 'high(USD)',
        '3a. low (USD)': 'low(USD)',
        '3b. low (USD)': 'low(USD)',
        '4a. close (USD)': 'close(USD)',
        '4b. close (USD)': 'close(USD)',
        '5. volume': 'volume',
        '6. market cap (USD)': 'market cap(USD)'
    })

    if (start_date == ""):
        start_date = None

    if (end_date == ""):
        end_date = None
    
    if (start_date or end_date):
        if (start_date and end_date):
            mask = (data.index > start_date) & (data.index <= end_date)
        elif (start_date):
            mask = (data.index > start_date)
        elif (end_date):
            mask = (data.index <= end_date)
        else:
            pass
        data = data[mask]

    data['timestamp'] = data.index.values.astype(str)
    response_dict = {"response":data.to_dict(orient="record")}
    return response_dict