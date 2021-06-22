import responses
from django.test import TestCase

from data_blocks.blocks.equity_data.main import run

# Create your tests here.


class GetEquityName(TestCase):
    @responses.activate
    def test_ok(self):
        ticker_name = "GOOG"

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

        self.assertEqual(response.json(), {"response": ["BA", "BAB"]})

    @responses.activate
    def test_empty_input(self):
        ticker_name = ""

        response = self.client.get(f"/DATA_BLOCK/1/equityName?name={ticker_name}")

        self.assertEqual(response.json(), {"response": []})

    @responses.activate
    def test_not_found(self):
        responses.add(
            responses.GET,
            f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=Ticker%20Name%20DNE&apikey=demo&datatype=json",
            json={"bestMatches": [],},
            status=200,
        )

        response = self.client.get(f"/DATA_BLOCK/1/equityName?name=Ticker Name DNE")

        self.assertEqual(response.json(), {"response": []})

    # TODO: It seems like there is no API limit
    def test_error_api_key_limit(self):
        pass


class GetDataType(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/dataType")

        self.assertEqual(response.json(), {"response": ["intraday", "daily_adjusted"]})


class GetInterval(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/interval")

        self.assertEqual(response.json(), {"response": ["1min"]})


class OutputSize(TestCase):
    def test_ok(self):
        response = self.client.get("/DATA_BLOCK/1/outputSize")

        self.assertEqual(response.json(), {"response": ["compact", "full"]})


class PostRun(TestCase):
    # def test_get_intraday_data_ok(self):
    #     payload = {
    #         'input': '',
    #         'output': '',
    #     }

    #     response = self.client.post('/DATA_BLOCK/1/run', payload)
    #     print (response.json())

    #     pass

    def test_get_intraday_data_error_cannot_find_ticker(self):
        pass

    def test_get_intraday_data_invalid_payload(self):
        pass


# class EquityDataBlock(TestCase):
#     def test_get_intraday_data(self):
#         request_payload = {
#             "input": {
#                 "equity_name": "AAPL",
#                 "data_type": "intraday",
#                 "interval": "1min",
#                 "outputsize": "full",
#                 "start_date": "",
#                 "end_date": "",
#             },
#             "output": {},
#         }

#         response = run(request_payload["input"])

#         assert True

#     def test_get_intraday_data_with_date_range(self):
#         # TODO: Fix the date range input, which is currently not working
#         request_payload = {
#             "input": {
#                 "equity_name": "AAPL",
#                 "data_type": "intraday",
#                 "interval": "1min",
#                 "outputsize": "full",
#                 "start_date": "2020-01-01",
#                 "end_date": "2021-01-01",
#             },
#             "output": {},
#         }

#         response = run(request_payload["input"])

#         print(response)

#         assert False
