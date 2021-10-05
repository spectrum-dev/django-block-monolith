import responses

from os import environ
from datetime import datetime
from django.test import TestCase

from data_store.helpers import get_all_weekdays
from data_store.interface import store_eod_data
from data_store.models import EquityDataStore

# Create your tests here.


class TestStoreEodData(TestCase):
    databases = "__all__"

    @responses.activate
    def test_base_case_ok(self):
        start_date = "2021-09-30"
        end_date = "2021-10-01"
        exchange = "US"

        dates_in_range = get_all_weekdays(
            start_date=datetime.fromisoformat(start_date),
            end_date=datetime.fromisoformat(end_date),
        )

        for date in dates_in_range:
            responses.add(
                responses.GET,
                f"https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={environ['EOD_HISTORICAL_DATA_API_KEY']}&fmt=json&date={date}",
                json=[
                    {
                        "code": "BBK",
                        "exchange_short_name": exchange,
                        "date": date,
                        "open": 0.505,
                        "high": 0.506,
                        "low": 0.501,
                        "close": 0.506,
                        "adjusted_close": 0.506,
                        "volume": 37791,
                    },
                ],
                status=200,
            )

        store_eod_data(start_date, end_date, exchange)

        assert EquityDataStore.objects.using("data_bank").all().count() == 2

    @responses.activate
    def test_same_data_inserted_updates_record_ok(self):
        start_date = "2021-09-30"
        end_date = "2021-10-01"
        exchange = "US"

        dates_in_range = get_all_weekdays(
            start_date=datetime.fromisoformat(start_date),
            end_date=datetime.fromisoformat(end_date),
        )

        for date in dates_in_range:
            responses.add(
                responses.GET,
                f"https://eodhistoricaldata.com/api/eod-bulk-last-day/{exchange}?api_token={environ['EOD_HISTORICAL_DATA_API_KEY']}&fmt=json&date={date}",
                json=[
                    {
                        "code": "BBK",
                        "exchange_short_name": exchange,
                        "date": date,
                        "open": 0.505,
                        "high": 0.506,
                        "low": 0.501,
                        "close": 0.506,
                        "adjusted_close": 0.506,
                        "volume": 37791,
                    },
                ],
                status=200,
            )

        store_eod_data(start_date, end_date, exchange)
        assert EquityDataStore.objects.using("data_bank").all().count() == 2

        store_eod_data(start_date, end_date, exchange)
        assert EquityDataStore.objects.using("data_bank").all().count() == 2
