import json
import responses

from django.test import TestCase

from blocks.event import event_ingestor

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


class GetCandlestick(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/candlestick")

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    "1min",
                    "5min",
                    "15min",
                    "30min",
                    "60min",
                    "1day",
                    "1week",
                    "1month",
                ]
            },
        )


class PostRun(TestCase):

    def setUp(self):
        self.payload = {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
        }
    
    @responses.activate
    def test_get_intraday_1min_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "1min",
                "start_date": "2021-06-21 19:58:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
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
                    "6. Time Zone": "US/Eastern",
                },
                "Time Series (1min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165",
                    },
                    "2021-06-21 19:59:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212",
                    },
                    "2021-06-21 19:58:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 132.4,
                        "high": 132.41,
                        "low": 132.4,
                        "close": 132.41,
                        "volume": 1485.0,
                        "timestamp": "2021-06-21T19:58:00.000000000",
                    },
                    {
                        "open": 132.39,
                        "high": 132.41,
                        "low": 132.38,
                        "close": 132.41,
                        "volume": 1212.0,
                        "timestamp": "2021-06-21T19:59:00.000000000",
                    },
                    {
                        "open": 132.38,
                        "high": 132.45,
                        "low": 132.38,
                        "close": 132.45,
                        "volume": 7165.0,
                        "timestamp": "2021-06-21T20:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_intraday_5min_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "5min",
                "start_date": "2021-06-21 19:50:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Intraday (5min) open, high, low, close prices and volume",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-21 20:00:00",
                    "4. Interval": "5min",
                    "5. Output Size": "Full size",
                    "6. Time Zone": "US/Eastern",
                },
                "Time Series (5min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165",
                    },
                    "2021-06-21 19:55:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212",
                    },
                    "2021-06-21 19:50:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 132.4,
                        "high": 132.41,
                        "low": 132.4,
                        "close": 132.41,
                        "volume": 1485.0,
                        "timestamp": "2021-06-21T19:50:00.000000000",
                    },
                    {
                        "open": 132.39,
                        "high": 132.41,
                        "low": 132.38,
                        "close": 132.41,
                        "volume": 1212.0,
                        "timestamp": "2021-06-21T19:55:00.000000000",
                    },
                    {
                        "open": 132.38,
                        "high": 132.45,
                        "low": 132.38,
                        "close": 132.45,
                        "volume": 7165.0,
                        "timestamp": "2021-06-21T20:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_intraday_15min_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "15min",
                "start_date": "2021-06-21 19:30:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=15min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Intraday (15min) open, high, low, close prices and volume",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-21 20:00:00",
                    "4. Interval": "15min",
                    "5. Output Size": "Full size",
                    "6. Time Zone": "US/Eastern",
                },
                "Time Series (15min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165",
                    },
                    "2021-06-21 19:45:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212",
                    },
                    "2021-06-21 19:30:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 132.4,
                        "high": 132.41,
                        "low": 132.4,
                        "close": 132.41,
                        "volume": 1485.0,
                        "timestamp": "2021-06-21T19:30:00.000000000",
                    },
                    {
                        "open": 132.39,
                        "high": 132.41,
                        "low": 132.38,
                        "close": 132.41,
                        "volume": 1212.0,
                        "timestamp": "2021-06-21T19:45:00.000000000",
                    },
                    {
                        "open": 132.38,
                        "high": 132.45,
                        "low": 132.38,
                        "close": 132.45,
                        "volume": 7165.0,
                        "timestamp": "2021-06-21T20:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_intraday_30min_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "30min",
                "start_date": "2021-06-21 19:00:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=30min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Intraday (30min) open, high, low, close prices and volume",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-21 20:00:00",
                    "4. Interval": "30min",
                    "5. Output Size": "Full size",
                    "6. Time Zone": "US/Eastern",
                },
                "Time Series (30min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165",
                    },
                    "2021-06-21 19:30:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212",
                    },
                    "2021-06-21 19:00:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 132.4,
                        "high": 132.41,
                        "low": 132.4,
                        "close": 132.41,
                        "volume": 1485.0,
                        "timestamp": "2021-06-21T19:00:00.000000000",
                    },
                    {
                        "open": 132.39,
                        "high": 132.41,
                        "low": 132.38,
                        "close": 132.41,
                        "volume": 1212.0,
                        "timestamp": "2021-06-21T19:30:00.000000000",
                    },
                    {
                        "open": 132.38,
                        "high": 132.45,
                        "low": 132.38,
                        "close": 132.45,
                        "volume": 7165.0,
                        "timestamp": "2021-06-21T20:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_intraday_60min_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "60min",
                "start_date": "2021-06-21 18:00:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=60min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Intraday (60min) open, high, low, close prices and volume",
                    "2. Symbol": "AAPL",
                    "3. Last Refreshed": "2021-06-21 20:00:00",
                    "4. Interval": "60min",
                    "5. Output Size": "Full size",
                    "6. Time Zone": "US/Eastern",
                },
                "Time Series (60min)": {
                    "2021-06-21 20:00:00": {
                        "1. open": "132.3800",
                        "2. high": "132.4500",
                        "3. low": "132.3800",
                        "4. close": "132.4500",
                        "5. volume": "7165",
                    },
                    "2021-06-21 19:00:00": {
                        "1. open": "132.3900",
                        "2. high": "132.4100",
                        "3. low": "132.3800",
                        "4. close": "132.4100",
                        "5. volume": "1212",
                    },
                    "2021-06-21 18:00:00": {
                        "1. open": "132.4000",
                        "2. high": "132.4100",
                        "3. low": "132.4000",
                        "4. close": "132.4100",
                        "5. volume": "1485",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 132.4,
                        "high": 132.41,
                        "low": 132.4,
                        "close": 132.41,
                        "volume": 1485.0,
                        "timestamp": "2021-06-21T18:00:00.000000000",
                    },
                    {
                        "open": 132.39,
                        "high": 132.41,
                        "low": 132.38,
                        "close": 132.41,
                        "volume": 1212.0,
                        "timestamp": "2021-06-21T19:00:00.000000000",
                    },
                    {
                        "open": 132.38,
                        "high": 132.45,
                        "low": 132.38,
                        "close": 132.45,
                        "volume": 7165.0,
                        "timestamp": "2021-06-21T20:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_intraday_data_error_cannot_find_ticker(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "TICKER_DNE",
                "candlestick": "1min",
                "start_date": "2021-06-21 19:58:00",
                "end_date": "2021-06-21 20:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TICKER_DNE&interval=1min&outputsize=full&apikey=demo&datatype=json",
            json={
                "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY."
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(response, {"response": []})

    @responses.activate
    def test_get_daily_adjusted_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "1day",
                "start_date": "2021-06-18 00:00:00",
                "end_date": "2021-06-22 00:00:00",
            },
            "outputs": {},
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
                    "5. Time Zone": "US/Eastern",
                },
                "Time Series (Daily)": {
                    "2021-06-22": {
                        "1. open": "132.1300",
                        "2. high": "134.0800",
                        "3. low": "131.6200",
                        "4. close": "133.9800",
                        "5. volume": "74783618",
                    },
                    "2021-06-21": {
                        "1. open": "130.3000",
                        "2. high": "132.4100",
                        "3. low": "129.2100",
                        "4. close": "132.3000",
                        "5. volume": "79663316",
                    },
                    "2021-06-18": {
                        "1. open": "130.7100",
                        "2. high": "131.5100",
                        "3. low": "130.2400",
                        "4. close": "130.4600",
                        "5. volume": "108953309",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 130.71,
                        "high": 131.51,
                        "low": 130.24,
                        "close": 130.46,
                        "volume": 108953309.0,
                        "timestamp": "2021-06-18T00:00:00.000000000",
                    },
                    {
                        "open": 130.3,
                        "high": 132.41,
                        "low": 129.21,
                        "close": 132.3,
                        "volume": 79663316.0,
                        "timestamp": "2021-06-21T00:00:00.000000000",
                    },
                    {
                        "open": 132.13,
                        "high": 134.08,
                        "low": 131.62,
                        "close": 133.98,
                        "volume": 74783618.0,
                        "timestamp": "2021-06-22T00:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_weekly_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "IBM",
                "candlestick": "1week",
                "start_date": "2021-07-16 00:00:00",
                "end_date": "2021-07-30 00:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Weekly Prices (open, high, low, close) and Volumes",
                    "2. Symbol": "IBM",
                    "3. Last Refreshed": "2021-07-30",
                    "4. Time Zone": "US/Eastern",
                },
                "Weekly Time Series": {
                    "2021-07-30": {
                        "1. open": "141.3900",
                        "2. high": "143.6400",
                        "3. low": "140.7900",
                        "4. close": "140.9600",
                        "5. volume": "16120616",
                    },
                    "2021-07-23": {
                        "1. open": "136.4500",
                        "2. high": "144.9200",
                        "3. low": "136.2089",
                        "4. close": "141.3400",
                        "5. volume": "34786264",
                    },
                    "2021-07-16": {
                        "1. open": "141.4300",
                        "2. high": "141.9599",
                        "3. low": "138.5900",
                        "4. close": "138.9000",
                        "5. volume": "18659679",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 141.43,
                        "high": 141.9599,
                        "low": 138.59,
                        "close": 138.9,
                        "volume": 18659679.0,
                        "timestamp": "2021-07-16T00:00:00.000000000",
                    },
                    {
                        "open": 136.45,
                        "high": 144.92,
                        "low": 136.2089,
                        "close": 141.34,
                        "volume": 34786264.0,
                        "timestamp": "2021-07-23T00:00:00.000000000",
                    },
                    {
                        "open": 141.39,
                        "high": 143.64,
                        "low": 140.79,
                        "close": 140.96,
                        "volume": 16120616.0,
                        "timestamp": "2021-07-30T00:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_monthly_data_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "IBM",
                "candlestick": "1month",
                "start_date": "2021-05-28 00:00:00",
                "end_date": "2021-07-30 00:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Monthly Prices (open, high, low, close) and Volumes",
                    "2. Symbol": "IBM",
                    "3. Last Refreshed": "2021-07-30",
                    "4. Time Zone": "US/Eastern",
                },
                "Monthly Time Series": {
                    "2021-07-30": {
                        "1. open": "146.9600",
                        "2. high": "147.5000",
                        "3. low": "136.2089",
                        "4. close": "140.9600",
                        "5. volume": "110625907",
                    },
                    "2021-06-30": {
                        "1. open": "145.0000",
                        "2. high": "152.8400",
                        "3. low": "143.0400",
                        "4. close": "146.5900",
                        "5. volume": "84365220",
                    },
                    "2021-05-28": {
                        "1. open": "143.8100",
                        "2. high": "148.5150",
                        "3. low": "140.9200",
                        "4. close": "143.7400",
                        "5. volume": "98036425",
                    },
                },
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {
                        "open": 143.81,
                        "high": 148.515,
                        "low": 140.92,
                        "close": 143.74,
                        "volume": 98036425.0,
                        "timestamp": "2021-05-28T00:00:00.000000000",
                    },
                    {
                        "open": 145.0,
                        "high": 152.84,
                        "low": 143.04,
                        "close": 146.59,
                        "volume": 84365220.0,
                        "timestamp": "2021-06-30T00:00:00.000000000",
                    },
                    {
                        "open": 146.96,
                        "high": 147.5,
                        "low": 136.2089,
                        "close": 140.96,
                        "volume": 110625907.0,
                        "timestamp": "2021-07-30T00:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_get_daily_adjusted_data_error_cannot_find_ticker(self):
        payload = {
            **self.payload,
            "inputs": {
                "equity_name": "TICKER_DNE",
                "candlestick": "1day",
                "start_date": "2021-06-18 00:00:00",
                "end_date": "2021-06-22 00:00:00",
            },
            "outputs": {},
        }

        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TICKER_DNE&outputsize=full&apikey=demo&datatype=json",
            json={
                "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY."
            },
            status=200,
        )

        response = event_ingestor(payload)

        self.assertDictEqual(response, {"response": []})