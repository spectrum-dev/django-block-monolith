
import json

from django.test.testcases import TestCase

class TestAndRun(TestCase):
    def test_only_one_param_passed_in(self):
        payload = {
            "input": {},
            "output": {
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}, {"timestamp": "01/07/2020", "order": "BUY"}, {"timestamp": "01/32/2020", "order": "BUY"}],
            },
        }
        
        response = self.client.post(
            "/LOGICAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        # TODO: Determine expected response
        self.assertDictEqual(response.json(), {"non_field_errors": ["You must pass in at least two streams of data"]})

    def test_simple_two_param_and(self):
        payload = {
            "input": {},
            "output": {
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}, {"timestamp": "01/07/2020", "order": "BUY"}, {"timestamp": "01/32/2020", "order": "BUY"}],
                "SIGNAL_BLOCK-1-2": [{"timestamp": "01/07/2020", "order": "BUY"}],
            },
        }

        response = self.client.post(
            "/LOGICAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )
        
        self.assertDictEqual(
            response.json(),
            {'response': [{'timestamp': '01/07/2020', 'order': 'BUY'}]}
        )

    def test_simple_three_param_and(self):
        payload = {
            "input": {},
            "output": {
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}, {"timestamp": "01/07/2020", "order": "BUY"}, {"timestamp": "01/21/2020", "order": "BUY"}],
                "SIGNAL_BLOCK-1-2": [{"timestamp": "01/07/2020", "order": "BUY"}, {"timestamp": "01/14/2020", "order": "BUY"}],
                "SIGNAL_BLOCK-1-3": [{"timestamp": "01/07/2020", "order": "BUY"}],
            },
        }
        
        response = self.client.post(
            "/LOGICAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {'response': [{'timestamp': '01/07/2020', 'order': 'BUY'}]}
        )

    def test_buy_sell_same_timestamp_does_not_trigger_intersect(self):
        payload = {
            "input": {},
            "output": {
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}, {"timestamp": "01/07/2020", "order": "BUY"}, {"timestamp": "01/21/2020", "order": "BUY"}],
                "SIGNAL_BLOCK-1-2": [{"timestamp": "01/07/2020", "order": "SELL"}, {"timestamp": "01/14/2020", "order": "BUY"}],
                "SIGNAL_BLOCK-1-3": [{"timestamp": "01/07/2020", "order": "BUY"}],
            },
        }

        response = self.client.post(
            "/LOGICAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )
        
        self.assertDictEqual(
            response.json(),
            {'response': []}
        )


