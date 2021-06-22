from django.test import TestCase

from data_blocks.blocks.equity_data.main import run

# Create your tests here.
class EquityDataBlock(TestCase):
    def test_get_intraday_data(self):
        request_payload = {
            "input": {
                "equity_name": "AAPL",
                "data_type": "intraday",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "",
                "end_date": "",
            },
            "output": {},
        }

        response = run(request_payload["input"])

        assert True

    def test_get_intraday_data_with_date_range(self):
        # TODO: Fix the date range input, which is currently not working
        request_payload = {
            "input": {
                "equity_name": "AAPL",
                "data_type": "intraday",
                "interval": "1min",
                "outputsize": "full",
                "start_date": "2020-01-01",
                "end_date": "2021-01-01",
            },
            "output": {},
        }

        response = run(request_payload["input"])

        print(response)

        assert False
