import logging
from datetime import datetime

from data_store.helpers import get_all_weekdays, make_eod_candlestick_request
from data_store.models import EquityDataStore


def store_eod_data(start_date: str, end_date: str):
    """
    Iterates through a fixed date range and pulls in data
    """

    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)

    # Check database to see what datetimes to start from
    dates_in_range = get_all_weekdays(start_date=start_date, end_date=end_date)

    for day in dates_in_range:
        logging.info(f'Processing data for {day}')
        records = []
        response = make_eod_candlestick_request(exchange="US", date=day)
        if response is not None:
            for ticker_result in response:
                records.append(
                    EquityDataStore(
                        datetime=day,
                        exchange="US",
                        ticker=ticker_result["code"],
                        open=ticker_result["open"],
                        high=ticker_result["high"],
                        low=ticker_result["low"],
                        close=ticker_result["close"],
                        adjusted_close=ticker_result["adjusted_close"],
                        volume=ticker_result["volume"],
                    )
                )

            try:
                EquityDataStore.objects.using("data_bank").bulk_create(
                    records, ignore_conflicts=True
                )
            except Exception as e:
                logging.error(e)
        
        logging.info(f'Processed data for {day}')
    
    return True


