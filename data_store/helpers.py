from datetime import timedelta
from os import environ

import requests

EOD_HISTORICAL_DATA_API_KEY = environ["EOD_HISTORICAL_DATA_API_KEY"]


def get_all_weekdays(start_date=None, end_date=None):
    """
    Gets a list of all weekdays in YYYY-MM-DD format

    Attributes
        start_date: Datetime of Start Date
        end_date: Datetime of End Date
    """

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    all_dates = []
    weekdays = [6, 7]
    for dt in daterange(start_date, end_date):
        if dt.isoweekday() not in weekdays:
            all_dates.append(dt.strftime("%Y-%m-%d"))

    return all_dates


def make_eod_candlestick_request(exchange="US", date=None):
    url = (
        f"https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={EOD_HISTORICAL_DATA_API_KEY}&fmt=json&date={date}"
        if date
        else f"https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={EOD_HISTORICAL_DATA_API_KEY}&fmt=json"
    )

    response = requests.get(url)
    response = response.json() if response.status_code == 200 else None

    return response
