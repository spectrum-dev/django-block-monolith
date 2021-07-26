import json

from django.test import TestCase

class GetSymbol(TestCase):
    def test_ok(self):
        response = self.client.get(
            "/DATA_BLOCK/2/cryptoName?name=btc"
        )

        self.assertDictEqual(
            response.json(),
            {'response': [{'value': 'BITBTC', 'label': 'BitBTC'}, {'value': 'BTC', 'label': 'Bitcoin'}, {'value': 'BTCB', 'label': 'Bitcoin BEP2'}, {'value': 'BTCD', 'label': 'BitcoinDark'}, {'value': 'BTCP', 'label': 'Bitcoin-Private'}, {'value': 'EBTC', 'label': 'eBTC'}, {'value': 'SBTC', 'label': 'Super-Bitcoin'}]}
        )
    
    def test_case_insensitive(self):
        response = self.client.get(
            "/DATA_BLOCK/2/cryptoName?name=Ethereum"
        )

        self.assertDictEqual(
            response.json(),
            {'response': [{'value': 'ETC', 'label': 'Ethereum-Classic'}, {'value': 'ETH', 'label': 'Ethereum'}, {'value': 'ETHD', 'label': 'Ethereum-Dark'}]}
        )

    def test_no_results(self):
        response = self.client.get(
            "/DATA_BLOCK/2/cryptoName?name=no-results"
        )

        self.assertDictEqual(
            response.json(),
            {'response': []}
        )

class PostRun(TestCase):
    def test_one_minute_candlestick_ok(self):
        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1min",
                "start_date": "2021-07-23 10:00:00",
                "end_date": "2021-07-23 10:05:00",
            },
            "output": {},
        }

        response = self.client.post(
            "/DATA_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(response.json(), {'response': [{'open': '32324.52000', 'high': '32336.75000', 'low': '32314.00000', 'close': '32332.70000', 'volume': 26, 'timestamp': '2021-07-23T10:00:00.000000000'}, {'open': '32332.71000', 'high': '32354.78000', 'low': '32323.01000', 'close': '32328.77000', 'volume': 29, 'timestamp': '2021-07-23T10:01:00.000000000'}, {'open': '32328.77000', 'high': '32332.53000', 'low': '32293.15000', 'close': '32309.62000', 'volume': 64, 'timestamp': '2021-07-23T10:02:00.000000000'}, {'open': '32309.63000', 'high': '32315.74000', 'low': '32233.24000', 'close': '32275.49000', 'volume': 122, 'timestamp': '2021-07-23T10:03:00.000000000'}, {'open': '32275.49000', 'high': '32298.02000', 'low': '32270.67000', 'close': '32290.62000', 'volume': 36, 'timestamp': '2021-07-23T10:04:00.000000000'}, {'open': '32290.61000', 'high': '32315.75000', 'low': '32288.61000', 'close': '32314.44000', 'volume': 17, 'timestamp': '2021-07-23T10:05:00.000000000'}]})

    def test_five_minute_candlestick_ok(self):
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

        self.assertDictEqual(response.json(), {'response': [{'open': '32483.51000', 'high': '32497.51000', 'low': '32427.68000', 'close': '32448.15000', 'volume': 110, 'timestamp': '2021-07-23T15:00:00.000000000'}, {'open': '32448.15000', 'high': '32469.60000', 'low': '32401.83000', 'close': '32433.34000', 'volume': 110, 'timestamp': '2021-07-23T15:05:00.000000000'}, {'open': '32433.34000', 'high': '32436.10000', 'low': '32393.45000', 'close': '32397.60000', 'volume': 86, 'timestamp': '2021-07-23T15:10:00.000000000'}]})

    def test_fifteen_minute_candlestick_ok(self):
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

        self.assertDictEqual(response.json(), {'response': [{'open': '32431.97000', 'high': '32495.00000', 'low': '32382.31000', 'close': '32406.32000', 'volume': 358, 'timestamp': '2021-07-23T13:00:00.000000000'}, {'open': '32406.32000', 'high': '32457.73000', 'low': '32364.72000', 'close': '32408.91000', 'volume': 330, 'timestamp': '2021-07-23T13:15:00.000000000'}, {'open': '32408.91000', 'high': '32474.99000', 'low': '32390.04000', 'close': '32451.04000', 'volume': 331, 'timestamp': '2021-07-23T13:30:00.000000000'}]})


    def test_thirty_minute_candlestick_ok(self):
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

        self.assertDictEqual(response.json(), {'response': [{'open': '32431.97000', 'high': '32495.00000', 'low': '32364.72000', 'close': '32408.91000', 'volume': 689, 'timestamp': '2021-07-23T13:00:00.000000000'}, {'open': '32408.91000', 'high': '32599.86000', 'low': '32390.04000', 'close': '32546.64000', 'volume': 953, 'timestamp': '2021-07-23T13:30:00.000000000'}, {'open': '32548.57000', 'high': '32575.20000', 'low': '32472.82000', 'close': '32533.82000', 'volume': 662, 'timestamp': '2021-07-23T14:00:00.000000000'}, {'open': '32533.82000', 'high': '32552.81000', 'low': '32420.00000', 'close': '32483.51000', 'volume': 504, 'timestamp': '2021-07-23T14:30:00.000000000'}, {'open': '32483.51000', 'high': '32497.51000', 'low': '32351.65000', 'close': '32354.20000', 'volume': 782, 'timestamp': '2021-07-23T15:00:00.000000000'}]})


    def test_sixty_minute_candlestick_ok(self):
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

        self.assertDictEqual(response.json(), {'response': [{'open': '32431.97000', 'high': '32599.86000', 'low': '32364.72000', 'close': '32546.64000', 'volume': 1642, 'timestamp': '2021-07-23T13:00:00.000000000'}, {'open': '32548.57000', 'high': '32575.20000', 'low': '32420.00000', 'close': '32483.51000', 'volume': 1167, 'timestamp': '2021-07-23T14:00:00.000000000'}, {'open': '32483.51000', 'high': '32497.51000', 'low': '32276.06000', 'close': '32315.00000', 'volume': 1586, 'timestamp': '2021-07-23T15:00:00.000000000'}]})

    def test_one_day_candlestick_ok(self):
        payload = {
            "input": {
                "crypto_name": "BTC",
                "candlestick": "1day",
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
                        "open": 37388.05,
                        "high": 38491.0,
                        "low": 35782.0,
                        "close": 36675.72,
                        "volume": 109527.284943,
                        "timestamp": "2021-06-10T00:00:00.000000000",
                    },
                    {
                        "open": 36677.83,
                        "high": 37680.4,
                        "low": 35936.77,
                        "close": 37331.98,
                        "volume": 78466.0053,
                        "timestamp": "2021-06-11T00:00:00.000000000",
                    },
                    {
                        "open": 37331.98,
                        "high": 37463.63,
                        "low": 34600.36,
                        "close": 35546.11,
                        "volume": 87717.54999,
                        "timestamp": "2021-06-12T00:00:00.000000000",
                    },
                    {
                        "open": 35546.12,
                        "high": 39380.0,
                        "low": 34757.0,
                        "close": 39020.57,
                        "volume": 86921.025555,
                        "timestamp": "2021-06-13T00:00:00.000000000",
                    },
                    {
                        "open": 39020.56,
                        "high": 41064.05,
                        "low": 38730.0,
                        "close": 40516.29,
                        "volume": 108522.391949,
                        "timestamp": "2021-06-14T00:00:00.000000000",
                    },
                    {
                        "open": 40516.28,
                        "high": 41330.0,
                        "low": 39506.4,
                        "close": 40144.04,
                        "volume": 80679.622838,
                        "timestamp": "2021-06-15T00:00:00.000000000",
                    },
                    {
                        "open": 40143.8,
                        "high": 40527.14,
                        "low": 38116.01,
                        "close": 38349.01,
                        "volume": 87771.976937,
                        "timestamp": "2021-06-16T00:00:00.000000000",
                    },
                    {
                        "open": 38349.0,
                        "high": 39559.88,
                        "low": 37365.0,
                        "close": 38092.97,
                        "volume": 79541.307119,
                        "timestamp": "2021-06-17T00:00:00.000000000",
                    },
                    {
                        "open": 38092.97,
                        "high": 38202.84,
                        "low": 35129.29,
                        "close": 35819.84,
                        "volume": 95228.042935,
                        "timestamp": "2021-06-18T00:00:00.000000000",
                    },
                    {
                        "open": 35820.48,
                        "high": 36457.0,
                        "low": 34803.52,
                        "close": 35483.72,
                        "volume": 68712.449461,
                        "timestamp": "2021-06-19T00:00:00.000000000",
                    },
                    {
                        "open": 35483.72,
                        "high": 36137.72,
                        "low": 33336.0,
                        "close": 35600.16,
                        "volume": 89878.17085,
                        "timestamp": "2021-06-20T00:00:00.000000000",
                    },
                    {
                        "open": 35600.17,
                        "high": 35750.0,
                        "low": 31251.23,
                        "close": 31608.93,
                        "volume": 168778.873159,
                        "timestamp": "2021-06-21T00:00:00.000000000",
                    },
                ]
            },
        )

    def test_one_week_candlestick_ok(self):
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
                        "open": 35796.31,
                        "high": 39380.0,
                        "low": 31000.0,
                        "close": 39020.57,
                        "volume": 700065.604915,
                        "timestamp": "2021-06-13T00:00:00.000000000",
                    },
                    {
                        "open": 39020.56,
                        "high": 41330.0,
                        "low": 33336.0,
                        "close": 35600.16,
                        "volume": 610333.962089,
                        "timestamp": "2021-06-20T00:00:00.000000000",
                    },
                ]
            },
        )

    def test_one_month_candlestick_ok(self):
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
                        "open": 58739.46,
                        "high": 64854.0,
                        "low": 46930.0,
                        "close": 57694.27,
                        "volume": 1993468.93801,
                        "timestamp": "2021-04-30T00:00:00.000000000",
                    },
                    {
                        "open": 57697.25,
                        "high": 59500.0,
                        "low": 30000.0,
                        "close": 37253.81,
                        "volume": 3536245.25657,
                        "timestamp": "2021-05-31T00:00:00.000000000",
                    },
                    {
                        "open": 37253.82,
                        "high": 41330.0,
                        "low": 28805.0,
                        "close": 35045.0,
                        "volume": 2901775.30592,
                        "timestamp": "2021-06-30T00:00:00.000000000",
                    },
                ]
            },
        )
