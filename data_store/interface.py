from datetime import date

from data_store.interface import get_weekdays, make_eod_candlestick_request
from data_store.models import EquityDataStore

def store_eod_data():
    """
        Iterates through a fixed date range and pulls in data
    """
    # Check database to see what datetimes to start from
    dates_in_range = get_weekdays(start_date=date(2020, 1, 1), end_date=date(2021, 10, 4))
    for day in dates_in_range:
        response = make_eod_candlestick_request(exchange="US", date=day)
        if response is not None:
            for ticker_result in response:
                EquityDataStore.objects.update_or_create(
                    date=day,
                    exchange="US",
                    ticker_name=ticker_result["code"],
                    open=ticker_result["open"],
                    high=ticker_result["high"],
                    low=ticker_result["low"],
                    close=ticker_result["close"],
                    adjusted_close=ticker_result["adjusted_close"],
                    volume=ticker_result["volume"],
                )
