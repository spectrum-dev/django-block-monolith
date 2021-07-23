import pandas as pd
from os import environ

from alpha_vantage.cryptocurrencies import CryptoCurrencies

def get_crypto_data(symbol, data_type, market="USD"):
    crypto = CryptoCurrencies(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    
    data, metadata = None, None
    if data_type in ["1min", "5min", "15min", "30min", "60min"]:
        # TODO: Implement the below endpoint manually
        # https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&outputsize=full&apikey=demo
        pass
    elif data_type == "1day":
        data, metadata = crypto.get_digital_currency_daily(symbol=symbol, market=market)
    elif data_type == "1week":
        data, metadata = crypto.get_digital_currency_weekly(symbol=symbol, market=market)
    elif data_type == "1month":
        data, metadata = crypto.get_digital_currency_monthly(symbol=symbol, market=market)
    else:
        raise Exception("Data Type is unimplemented")
    
    # Renames columns from defalt provided by AlphaVantage to more standard terms
    data = data.rename(
        columns={
            "1a. open (USD)": "open",
            "2a. high (USD)": "high",
            "3a. low (USD)": "low",
            "4a. close (USD)": "close",
            "5. volume": "volume",
        }
    )

    data = data.drop(columns = ["1b. open (USD)", "2b. high (USD)", "3b. low (USD)", "4b. close (USD)", "6. market cap (USD)"])

    # if start_date == "":
    #     start_date = None

    # if end_date == "":
    #     end_date = None

    # if start_date or end_date:
    #     if start_date and end_date:
    #         mask = (data.index > start_date) & (data.index <= end_date)
    #     elif start_date:
    #         mask = data.index > start_date
    #     elif end_date:
    #         mask = data.index <= end_date
    #     else:
    #         pass
    #     data = data[mask]

    return data
