import json
import responses

from django.test import TestCase

from data_blocks.blocks.equity_data.main import run

# Create your tests here.


class GetEquityName(TestCase):
    @responses.activate
    def test_ok(self):
        ticker_name = "BA"

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker_name}&apikey=demo&datatype=json",
            json={
                "bestMatches": [
                    {
                        "1. symbol": "BA",
                        "2. name": "Boeing Company",
                        "3. type": "Equity",
                        "4. region": "United States",
                        "5. marketOpen": "09:30",
                        "6. marketClose": "16:00",
                        "7. timezone": "UTC-04",
                        "8. currency": "USD",
                        "9. matchScore": "1.0000",
                    },
                    {
                        "1. symbol": "BAB",
                        "2. name": "Invesco Taxable Municipal Bond ETF",
                        "3. type": "ETF",
                        "4. region": "United States",
                        "5. marketOpen": "09:30",
                        "6. marketClose": "16:00",
                        "7. timezone": "UTC-04",
                        "8. currency": "USD",
                        "9. matchScore": "0.8000",
                    },
                ],
            },
            status=200,
        )

        response = self.client.get(f"/DATA_BLOCK/1/equityName?name={ticker_name}")

        self.assertDictEqual(response.json(), {"response": ["BA", "BAB"]})

    @responses.activate
    def test_empty_input(self):
        ticker_name = ""

        response = self.client.get(f"/DATA_BLOCK/1/equityName?name={ticker_name}")

        self.assertDictEqual(response.json(), {"response": []})

    @responses.activate
    def test_not_found(self):
        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=Ticker%20Name%20DNE&apikey=demo&datatype=json",
            json={
                "bestMatches": [],
            },
            status=200,
        )

        response = self.client.get(f"/DATA_BLOCK/1/equityName?name=Ticker Name DNE")

        self.assertDictEqual(response.json(), {"response": []})

    # TODO: It seems like there is no API limit
    def test_error_api_key_limit(self):
        pass


class GetDataType(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/dataType")

        self.assertDictEqual(response.json(), {"response": ["intraday", "daily_adjusted"]})


class GetInterval(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/interval")

        self.assertDictEqual(response.json(), {"response": ["1min"]})


class OutputSize(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/outputSize")

        self.assertDictEqual(response.json(), {"response": ["compact", "full"]})


class PostRun(TestCase):
    @responses.activate
    def test_get_intraday_data_ok(self):
        payload = {
            "input": {
                "equity_name": "AAPL",
                "data_type": "intraday",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2021-06-21 19:58:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "output": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=1min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Intraday (1min) open, high, low, close prices and volume",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-21 20:00:00",
                    "4. Interval": "1min",
                    "5. Output Size": "Full size",
                    "6. Time Zone": "US/Eastern"
                },
                "Time Series (1min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165"
                    },
                    "2021-06-21 19:59:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212"
                    },
                    "2021-06-21 19:58:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485"
                    },
                }
            },
            status=200,
        )

        response = self.client.post("/DATA_BLOCK/1/run", json.dumps(payload), content_type="application/json")
        
        self.assertDictEqual(
            response.json(),
            {'response': [{'open': 132.38, 'high': 132.45, 'low': 132.38, 'close': 132.45, 'volume': 7165.0, 'timestamp': '2021-06-21T20:00:00.000000000'}, {'open': 132.39, 'high': 132.41, 'low': 132.38, 'close': 132.41, 'volume': 1212.0, 'timestamp': '2021-06-21T19:59:00.000000000'}]}
        )

    @responses.activate
    def test_get_intraday_data_error_cannot_find_ticker(self):
        payload = {
            "input": {
                "equity_name": "TICKER_DNE",
                "data_type": "intraday",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2021-06-21 19:58:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "output": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TICKER_DNE&interval=1min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY."
            },
            status=200,
        )

        response = self.client.post("/DATA_BLOCK/1/run", json.dumps(payload), content_type="application/json")

        self.assertDictEqual(
            response.json(),
            {'response': []}
        )
    
    @responses.activate
    def test_get_daily_adjusted_data_ok(self):
        payload = {
            "input": {
                "equity_name": "AAPL",
                "data_type": "daily_adjusted",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2021-06-18 00:00:00",
                "end_date": "2021-06-22 00:00:00",
            },
            "output": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=full&apikey=demo&datatype=json",
            json={
                 "Meta Data": {
                    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-22",
                    "4. Output Size": "Full size",
                    "5. Time Zone": "US/Eastern"
                },
                "Time Series (Daily)": {
                    "2021-06-22": {
                        "1. open": "132.1300",
                        "2. high": "134.0800",
                        "3. low": "131.6200",
                        "4. close": "133.9800",
                        "5. volume": "74783618"
                    },
                    "2021-06-21": {
                        "1. open": "130.3000",
                        "2. high": "132.4100",
                        "3. low": "129.2100",
                        "4. close": "132.3000",
                        "5. volume": "79663316"
                    },
                    "2021-06-18": {
                        "1. open": "130.7100",
                        "2. high": "131.5100",
                        "3. low": "130.2400",
                        "4. close": "130.4600",
                        "5. volume": "108953309"
                    }
                }
            },
            status=200
        )

        response = self.client.post("/DATA_BLOCK/1/run", json.dumps(payload), content_type="application/json")

        self.assertDictEqual(
            response.json(),
            {'response': [{'open': 132.13, 'high': 134.08, 'low': 131.62, 'close': 133.98, 'volume': 74783618.0, 'timestamp': '2021-06-22T00:00:00.000000000'}, {'open': 130.3, 'high': 132.41, 'low': 129.21, 'close': 132.3, 'volume': 79663316.0, 'timestamp': '2021-06-21T00:00:00.000000000'}]}
        )

    @responses.activate
    def test_get_daily_adjusted_data_error_cannot_find_ticker(self):
        payload = {
            "input": {
                "equity_name": "TICKER_DNE",
                "data_type": "daily_adjusted",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2021-06-18 00:00:00",
                "end_date": "2021-06-22 00:00:00",
            },
            "output": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TICKER_DNE&outputsize=full&apikey=demo&datatype=json",
            json={
                "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY."
            },
            status=200,
        )

        response = self.client.post("/DATA_BLOCK/1/run", json.dumps(payload), content_type="application/json")

        self.assertDictEqual(
            response.json(),
            {'response': []}
        )

    def test_get_stock_data_end_date_preceeds_start_date(self):
        payload = {
            "input": {
                "equity_name": "TICKER_DNE",
                "data_type": "daily_adjusted",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2021-06-22 00:00:00",
                "end_date": "2021-06-18 00:00:00",
            },
            "output": {},
        }

        response = self.client.post("/DATA_BLOCK/1/run", json.dumps(payload), content_type="application/json")

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['finish must occur after start']}
        )