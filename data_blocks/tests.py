from django.test import TestCase

from data_blocks.blocks.equity_data_block.main import run
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
            "output": {}
        }

        response = run(request_payload["input"])

        assert False

