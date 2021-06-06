import pandas as pd
from os import environ

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

def get_ticker_data(ticker, data_type='intraday', interval='1min', outputsize='full', start_date=None, end_date=None):
    # TODO: Swap out with AlphaVantage Key
    ts = TimeSeries(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data, meta_data = None, None
    if (data_type == "intraday"):
        data, meta_data = ts.get_intraday(ticker, interval=interval, outputsize=outputsize)
    elif (data_type == "daily_adjusted"):
        data, meta_data = ts.get_daily(ticker, outputsize=outputsize)
    else:
        raise f"Data Type: {data_type}"

    # Renames columns from defalt provided by AlphaVantage to more standard terms
    data = data.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
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

def search_ticker(keyword):
    ts = TimeSeries(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data, meta_data = ts.get_symbol_search(keywords=[keyword])
    data = data['1. symbol'].tolist()
    return {"response": data}

def get_company_overview(ticker):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data, _ = fd.get_company_overview(ticker)
    return data.to_dict(orient="record")[0]

def get_income_statement(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data = None
    if (time_period == "annual"):
        data, _ = fd.get_income_statement_annual(ticker)
    elif (time_period == "quarterly"):
        data, _ = fd.get_income_statement_quarterly(ticker)
    else:
        pass
    
    return data.to_dict(orient="record")[0]

def get_balance_sheet(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data = None
    if (time_period == "annual"):
        data, _ = fd.get_balance_sheet_annual(ticker)
    elif (time_period == "quarterly"):
        data, _ = fd.get_balance_sheet_quarterly(ticker)
    else:
        pass
    
    return data.to_dict(orient="record")[0]

def get_cash_flow(ticker, time_period="annual"):
    fd = FundamentalData(key=environ["ALPHA_VANTAGE_API_KEY"], output_format='pandas')
    data = None
    if (time_period == "annual"):
        data, _ = fd.get_cash_flow_annual(ticker)
    elif (time_period == "quarterly"):
        data, _ = fd.get_cash_flow_quarterly(ticker)
    else:
        pass

    return data.to_dict(orient="record")[0]
