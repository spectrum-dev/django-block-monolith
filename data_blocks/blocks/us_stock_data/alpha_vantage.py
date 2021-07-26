import pandas as pd
from os import environ

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData


def get_us_stock_data(symbol, data_type):
    try:
        ts = TimeSeries(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")

        data, metadata = None, None
        if data_type in ["1min", "5min", "15min", "30min", "60min"]:
            data, meta_data = ts.get_intraday(
                symbol, interval=data_type, outputsize="full"
            )
        elif data_type == "1day":
            data, meta_data = ts.get_daily(symbol, outputsize="full")
        elif data_type == "1week":
            data, meta_data = ts.get_weekly(symbol)
        elif data_type == "1month":
            data, meta_data = ts.get_monthly(symbol)
        else:
            raise Exception("Data type is unimplemented")

        data = data.rename(
            columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume",
            }
        )

        data = data.sort_index()

        return data
    except ValueError:
        return None


def search_ticker(keyword):
    ts = TimeSeries(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    data, meta_data = ts.get_symbol_search(keywords=[keyword])

    if data.empty:
        data = []
    else:
        data = data["1. symbol"].tolist()

    return {"response": data}


def get_company_overview(ticker):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    data, _ = fd.get_company_overview(ticker)
    return data.to_dict(orient="record")[0]


def get_income_statement(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    data = None
    if time_period == "annual":
        data, _ = fd.get_income_statement_annual(ticker)
    elif time_period == "quarterly":
        data, _ = fd.get_income_statement_quarterly(ticker)
    else:
        pass

    return data.to_dict(orient="record")[0]


def get_balance_sheet(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    data = None
    if time_period == "annual":
        data, _ = fd.get_balance_sheet_annual(ticker)
    elif time_period == "quarterly":
        data, _ = fd.get_balance_sheet_quarterly(ticker)
    else:
        pass

    return data.to_dict(orient="record")[0]


def get_cash_flow(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format="pandas")
    data = None
    if time_period == "annual":
        data, _ = fd.get_cash_flow_annual(ticker)
    elif time_period == "quarterly":
        data, _ = fd.get_cash_flow_quarterly(ticker)
    else:
        pass

    return data.to_dict(orient="record")[0]
