import json
import responses

from django.test import TestCase

class PostRun(TestCase):
    def test_ok(self):
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

        print (response.json())

        assert False