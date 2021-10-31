from os import environ

from alpha_vantage.timeseries import TimeSeries


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
