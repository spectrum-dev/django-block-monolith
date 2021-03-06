from django.test import TestCase

import data_store.factories
from blocks.event import event_ingestor


class RunScreenerData(TestCase):
    databases = "__all__"

    def setUp(self):
        self.payload = {
            "blockType": "BULK_DATA_BLOCK",
            "blockId": 1,
        }

    def test_single_ticker_in_db(self):
        data_store.factories.EquityDataStoreFactory(
            ticker="AAPL", datetime="2021-09-29 00:00:00"
        )
        data_store.factories.EquityDataStoreFactory(
            ticker="AAPL", datetime="2021-09-30 00:00:00"
        )
        data_store.factories.EquityDataStoreFactory(
            ticker="AAPL", datetime="2021-10-01 00:00:00"
        )

        payload = {
            **self.payload,
            "inputs": {
                "exchange_name": "US",
                "candlestick": "1day",
                "start_date": "2021-09-30 00:00:00",
                "end_date": "2021-10-01 00:00:00",
            },
            "outputs": {},
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
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
            },
        )

    def test_no_data_in_range(self):
        payload = {
            **self.payload,
            "inputs": {
                "exchange_name": "US",
                "candlestick": "1day",
                "start_date": "2021-09-30 00:00:00",
                "end_date": "2021-10-01 00:00:00",
            },
            "outputs": {},
        }

        response = event_ingestor(payload)

        self.assertDictEqual(response, {})
