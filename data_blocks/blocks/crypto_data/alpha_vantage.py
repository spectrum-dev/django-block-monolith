import pandas as pd
from os import environ
import requests

from alpha_vantage.cryptocurrencies import CryptoCurrencies


def get_crypto_data(symbol, data_type, market="USD"):
    crypto = CryptoCurrencies(
        key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas"
    )

    data, metadata = None, None
    if data_type in ["1min", "5min", "15min", "30min", "60min"]:
        url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}&market={market}&interval={data_type}&outputsize=full&apikey={environ["ALPHA_VANTAGE_API_KEY"]}'

        resp = requests.get(url)
        resp = resp.json()
        resp_keys = list(resp.keys())

        data = resp[resp_keys[1]]

        data = pd.DataFrame().from_dict(data, orient="index")
        data.index = pd.to_datetime(data.index)
    elif data_type == "1day":
        data, metadata = crypto.get_digital_currency_daily(symbol=symbol, market=market)
    elif data_type == "1week":
        data, metadata = crypto.get_digital_currency_weekly(
            symbol=symbol, market=market
        )
    elif data_type == "1month":
        data, metadata = crypto.get_digital_currency_monthly(
            symbol=symbol, market=market
        )

    if data_type in ["1min", "5min", "15min", "30min", "60min"]:
        data = data.rename(
            columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume",
            }
        )
    else:
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

        data = data.drop(
            columns=[
                "1b. open (USD)",
                "2b. high (USD)",
                "3b. low (USD)",
                "4b. close (USD)",
                "6. market cap (USD)",
            ]
        )

    data = data.sort_index()

    return data
