import logging
from datetime import datetime, date

from data_store.helpers import get_all_weekdays, make_eod_candlestick_request
from data_store.models import EquityDataStore


def get_date_range_of_missing_data(exchange):
    last_saved_date = (
        EquityDataStore.objects.order_by("datetime")
        .filter(exchange=exchange)
        .values_list("datetime")
        .distinct()
        .last()
    )
    last_saved_date = last_saved_date[0]

    current_date = datetime.today()

    # Removes timezone awareness
    last_saved_date = last_saved_date.replace(tzinfo=None)
    current_date = current_date.replace(tzinfo=None)

    return last_saved_date, current_date


def store_eod_data(start_date, end_date, exchange):
    """
    Iterates through a fixed date range and pulls in data
    """

    # Check database to see what datetimes to start from
    dates_in_range = get_all_weekdays(start_date=start_date, end_date=end_date)

    for day in dates_in_range:
        logging.info(f"Processing data for {day}")
        records = []
        response = make_eod_candlestick_request(exchange=exchange, date=day)
        if response is not None:
            for ticker_result in response:
                records.append(
                    EquityDataStore(
                        datetime=day,
                        exchange=exchange,
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
                    records, ignore_conflicts=True, batch_size=100
                )
            except Exception as e:
                logging.error(e)

        logging.info(f"Processed data for {day}")

    return True
