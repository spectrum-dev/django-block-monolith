from django.test import TestCase

from data_blocks.blocks.screener_data.main import run
from data_store.models import EquityDataStore
from data_store.factories import EquityDataStoreFactory


class GetCandlestick(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/3/exchange")

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    "US",
                    "KLSE",
                ]
            },
        )


class GetCandlestick(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/3/candlestick")

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    "1day",
                ]
            },
        )


class RunScreenerData(TestCase):
    databases = "__all__"

    def test_single_ticker_in_db(self):
        EquityDataStoreFactory(ticker="AAPL", datetime="2021-09-29 00:00:00")
        EquityDataStoreFactory(ticker="AAPL", datetime="2021-09-30 00:00:00")
        EquityDataStoreFactory(ticker="AAPL", datetime="2021-10-01 00:00:00")

        input = {
            "exchange_name": "US",
            "candlestick": "1day",
            "start_date": "2021-09-30 00:00:00",
            "end_date": "2021-10-01 00:00:00",
        }

        response = run(input)

        assert response == {
            "AAPL": [
                {
                    "timestamp": "2021-09-30 00:00:00",
                    "open": 0.0,
                    "high": 0.0,
                    "low": 0.0,
                    "close": 0.0,
                    "adjusted_close": 0.0,
                    "volume": 0.0,
                },
                {
                    "timestamp": "2021-10-01 00:00:00",
                    "open": 0.0,
                    "high": 0.0,
                    "low": 0.0,
                    "close": 0.0,
                    "adjusted_close": 0.0,
                    "volume": 0.0,
                },
            ]
        }

    def test_no_data_in_range(self):
        input = {
            "exchange_name": "US",
            "candlestick": "1day",
            "start_date": "2021-09-30 00:00:00",
            "end_date": "2021-10-01 00:00:00",
        }

        response = run(input)

        assert response == {}
