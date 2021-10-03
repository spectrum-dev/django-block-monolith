import requests
from os import environ

from datetime import timedelta, date


EOD_HISTORICAL_DATA_API_KEY = environ["EOD_HISTORICAL_DATA_API_KEY"]


def get_weekdays(start_date: date, end_date: date):
    """
        Gets a list of all weekdays in YYYY-MM-DD format

        Attributes
            start_date: Datetime of Start Date
            end_date: Datetime of End Date
    """
    response = []
    weekends = [6, 7]
    for dt in _get_date_range(start_date, end_date):
        if dt.isoweekday() not in weekends:
            response.append(dt.strftime("%Y-%m-%d"))
    
    return response


def _get_date_range(date_one, date_two):
    """
        Helper Function to get the integer index of a day within the range
    """
    for n in range(int ((date_one - date_two).days)+1):
        yield date_one + timedelta(n)


def make_eod_candlestick_request(exchange="US", date=None):
    url = f'https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={EOD_HISTORICAL_DATA_API_KEY}&fmt=json&date={date}' if date else f'https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={EOD_HISTORICAL_DATA_API_KEY}&fmt=json'
    
    response = requests.get(url)
    response = response.json() if response.status_code == 200 else None

    return response