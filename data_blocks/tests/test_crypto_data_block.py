import json
import responses

from django.test import TestCase


class GetSymbol(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/2/cryptoName?name=btc")

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"value": "BITBTC", "label": "BitBTC (BITBTC)"},
                    {"value": "BTC", "label": "Bitcoin (BTC)"},
                    {"value": "BTCB", "label": "Bitcoin BEP2 (BTCB)"},
                    {"value": "BTCD", "label": "BitcoinDark (BTCD)"},
                    {"value": "BTCP", "label": "Bitcoin-Private (BTCP)"},
                    {"value": "EBTC", "label": "eBTC (EBTC)"},
                    {"value": "SBTC", "label": "Super-Bitcoin (SBTC)"},
                ]
            },
        )

    def test_case_insensitive(self):
        response = self.client.get("/DATA_BLOCK/2/cryptoName?name=Ethereum")

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"value": "ETC", "label": "Ethereum-Classic (ETC)"},
                    {"value": "ETH", "label": "Ethereum (ETH)"},
                    {"value": "ETHD", "label": "Ethereum-Dark (ETHD)"},
                ]
            },
        )

    def test_no_results(self):
        response = self.client.get("/DATA_BLOCK/2/cryptoName?name=no-results")

        self.assertDictEqual(response.json(), {"response": []})


class GetCandlestick(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/2/candlestick")

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
    @responses.activate
    def test_one_minute_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=1min&outputsize=full&apikey=demo",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series Crypto (1min)": {
                    "2021-07-23 10:00:00": {
                        "1. open": "32324.52000",
                        "2. high": "32336.75000",
                        "3. low": "32314.00000",
                        "4. close": "32332.70000",
                        "5. volume": 26,
                    },
                    "2021-07-23 10:01:00": {
                        "1. open": "32332.71000",
                        "2. high": "32354.78000",
                        "3. low": "32323.01000",
                        "4. close": "32328.77000",
                        "5. volume": 29,
                    },
                    "2021-07-23 10:02:00": {
                        "1. open": "32328.77000",
                        "2. high": "32332.53000",
                        "3. low": "32293.15000",
                        "4. close": "32309.62000",
                        "5. volume": 64,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1min",
                "start_date": "2021-07-23 10:00:00",
                "end_date": "2021-07-23 10:02:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": "32324.52000",
                        "high": "32336.75000",
                        "low": "32314.00000",
                        "close": "32332.70000",
                        "volume": 26,
                        "timestamp": "2021-07-23T10:00:00.000000000",
                    },
                    {
                        "open": "32332.71000",
                        "high": "32354.78000",
                        "low": "32323.01000",
                        "close": "32328.77000",
                        "volume": 29,
                        "timestamp": "2021-07-23T10:01:00.000000000",
                    },
                    {
                        "open": "32328.77000",
                        "high": "32332.53000",
                        "low": "32293.15000",
                        "close": "32309.62000",
                        "volume": 64,
                        "timestamp": "2021-07-23T10:02:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_five_minute_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=5min&outputsize=full&apikey=demo",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series Crypto (5min)": {
                    "2021-07-23 15:00:00": {
                        "1. open": "32324.52000",
                        "2. high": "32336.75000",
                        "3. low": "32314.00000",
                        "4. close": "32332.70000",
                        "5. volume": 26,
                    },
                    "2021-07-23 15:05:00": {
                        "1. open": "32332.71000",
                        "2. high": "32354.78000",
                        "3. low": "32323.01000",
                        "4. close": "32328.77000",
                        "5. volume": 29,
                    },
                    "2021-07-23 15:10:00": {
                        "1. open": "32328.77000",
                        "2. high": "32332.53000",
                        "3. low": "32293.15000",
                        "4. close": "32309.62000",
                        "5. volume": 64,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "5min",
                "start_date": "2021-07-23 15:00:00",
                "end_date": "2021-07-23 15:10:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": "32324.52000",
                        "high": "32336.75000",
                        "low": "32314.00000",
                        "close": "32332.70000",
                        "volume": 26,
                        "timestamp": "2021-07-23T15:00:00.000000000",
                    },
                    {
                        "open": "32332.71000",
                        "high": "32354.78000",
                        "low": "32323.01000",
                        "close": "32328.77000",
                        "volume": 29,
                        "timestamp": "2021-07-23T15:05:00.000000000",
                    },
                    {
                        "open": "32328.77000",
                        "high": "32332.53000",
                        "low": "32293.15000",
                        "close": "32309.62000",
                        "volume": 64,
                        "timestamp": "2021-07-23T15:10:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_fifteen_minute_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=15min&outputsize=full&apikey=demo",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series Crypto (15min)": {
                    "2021-07-23 13:00:00": {
                        "1. open": "32324.52000",
                        "2. high": "32336.75000",
                        "3. low": "32314.00000",
                        "4. close": "32332.70000",
                        "5. volume": 26,
                    },
                    "2021-07-23 13:15:00": {
                        "1. open": "32332.71000",
                        "2. high": "32354.78000",
                        "3. low": "32323.01000",
                        "4. close": "32328.77000",
                        "5. volume": 29,
                    },
                    "2021-07-23 13:30:00": {
                        "1. open": "32328.77000",
                        "2. high": "32332.53000",
                        "3. low": "32293.15000",
                        "4. close": "32309.62000",
                        "5. volume": 64,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "15min",
                "start_date": "2021-07-23 13:00:00",
                "end_date": "2021-07-23 13:30:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": "32324.52000",
                        "high": "32336.75000",
                        "low": "32314.00000",
                        "close": "32332.70000",
                        "volume": 26,
                        "timestamp": "2021-07-23T13:00:00.000000000",
                    },
                    {
                        "open": "32332.71000",
                        "high": "32354.78000",
                        "low": "32323.01000",
                        "close": "32328.77000",
                        "volume": 29,
                        "timestamp": "2021-07-23T13:15:00.000000000",
                    },
                    {
                        "open": "32328.77000",
                        "high": "32332.53000",
                        "low": "32293.15000",
                        "close": "32309.62000",
                        "volume": 64,
                        "timestamp": "2021-07-23T13:30:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_thirty_minute_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=30min&outputsize=full&apikey=demo",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series Crypto (1min)": {
                    "2021-07-23 13:00:00": {
                        "1. open": "32324.52000",
                        "2. high": "32336.75000",
                        "3. low": "32314.00000",
                        "4. close": "32332.70000",
                        "5. volume": 26,
                    },
                    "2021-07-23 13:30:00": {
                        "1. open": "32332.71000",
                        "2. high": "32354.78000",
                        "3. low": "32323.01000",
                        "4. close": "32328.77000",
                        "5. volume": 29,
                    },
                    "2021-07-23 14:00:00": {
                        "1. open": "32328.77000",
                        "2. high": "32332.53000",
                        "3. low": "32293.15000",
                        "4. close": "32309.62000",
                        "5. volume": 64,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "30min",
                "start_date": "2021-07-23 13:00:00",
                "end_date": "2021-07-23 15:00:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": "32324.52000",
                        "high": "32336.75000",
                        "low": "32314.00000",
                        "close": "32332.70000",
                        "volume": 26,
                        "timestamp": "2021-07-23T13:00:00.000000000",
                    },
                    {
                        "open": "32332.71000",
                        "high": "32354.78000",
                        "low": "32323.01000",
                        "close": "32328.77000",
                        "volume": 29,
                        "timestamp": "2021-07-23T13:30:00.000000000",
                    },
                    {
                        "open": "32328.77000",
                        "high": "32332.53000",
                        "low": "32293.15000",
                        "close": "32309.62000",
                        "volume": 64,
                        "timestamp": "2021-07-23T14:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_sixty_minute_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=60min&outputsize=full&apikey=demo",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series Crypto (1min)": {
                    "2021-07-23 13:00:00": {
                        "1. open": "32324.52000",
                        "2. high": "32336.75000",
                        "3. low": "32314.00000",
                        "4. close": "32332.70000",
                        "5. volume": 26,
                    },
                    "2021-07-23 14:00:00": {
                        "1. open": "32332.71000",
                        "2. high": "32354.78000",
                        "3. low": "32323.01000",
                        "4. close": "32328.77000",
                        "5. volume": 29,
                    },
                    "2021-07-23 15:00:00": {
                        "1. open": "32328.77000",
                        "2. high": "32332.53000",
                        "3. low": "32293.15000",
                        "4. close": "32309.62000",
                        "5. volume": 64,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "60min",
                "start_date": "2021-07-23 13:00:00",
                "end_date": "2021-07-23 15:00:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": "32324.52000",
                        "high": "32336.75000",
                        "low": "32314.00000",
                        "close": "32332.70000",
                        "volume": 26,
                        "timestamp": "2021-07-23T13:00:00.000000000",
                    },
                    {
                        "open": "32332.71000",
                        "high": "32354.78000",
                        "low": "32323.01000",
                        "close": "32328.77000",
                        "volume": 29,
                        "timestamp": "2021-07-23T14:00:00.000000000",
                    },
                    {
                        "open": "32328.77000",
                        "high": "32332.53000",
                        "low": "32293.15000",
                        "close": "32309.62000",
                        "volume": 64,
                        "timestamp": "2021-07-23T15:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_one_day_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series (Digital Currency Daily)": {
                    "2021-06-10 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                    "2021-06-11 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                    "2021-06-12 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1day",
                "start_date": "2021-06-10 00:00:00",
                "end_date": "2021-06-12 00:00:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-10T00:00:00.000000000",
                    },
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-11T00:00:00.000000000",
                    },
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-12T00:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_one_week_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=USD&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series (Digital Currency Weekly)": {
                    "2021-06-13 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                    "2021-06-20 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1week",
                "start_date": "2021-06-10 00:00:00",
                "end_date": "2021-06-21 00:00:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-13T00:00:00.000000000",
                    },
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-20T00:00:00.000000000",
                    },
                ]
            },
        )

    @responses.activate
    def test_one_month_candlestick_ok(self):
        responses.add(
            responses.GET,
            "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=USD&apikey=demo&datatype=json",
            json={
                "Meta Data": {
                    "1. Information": "Crypto Intraday (1min) Time Series",
                    "2. Digital Currency Code": "BTC",
                    "3. Digital Currency Name": "Bitcoin",
                    "4. Market Code": "USD",
                    "5. Market Name": "United States Dollar",
                    "6. Last Refreshed": "2021-07-26 07:07:00",
                    "7. Interval": "1min",
                    "8. Output Size": "Full size",
                    "9. Time Zone": "UTC",
                },
                "Time Series (Digital Currency Monthly)": {
                    "2021-04-30 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                    "2021-05-31 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                    "2021-06-30 00:00:00": {
                        "1a. open (USD)": "32324.52000",
                        "1b. open (USD)": "32324.52000",
                        "2a. high (USD)": "32336.75000",
                        "2b. high (USD)": "32336.75000",
                        "3a. low (USD)": "32314.00000",
                        "3b. low (USD)": "32314.00000",
                        "4a. close (USD)": "32332.70000",
                        "4b. close (USD)": "32332.70000",
                        "5. volume (USD)": 26,
                        "6. market cap (USD)": 26,
                    },
                },
            },
            status=200,
        )

        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1month",
                "start_date": "2021-04-01 00:00:00",
                "end_date": "2021-07-01 00:00:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-04-30T00:00:00.000000000",
                    },
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-05-31T00:00:00.000000000",
                    },
                    {
                        "open": 32324.52,
                        "high": 32336.75,
                        "low": 32314.0,
                        "close": 32332.7,
                        "5. volume (USD)": 26.0,
                        "timestamp": "2021-06-30T00:00:00.000000000",
                    },
                ]
            },
        )
