import json

from django.test.testcases import TestCase


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/5/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class TestOrRun(TestCase):
    def test_only_one_param_passed_in(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/32/2020", "order": "BUY"},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {"non_field_errors": ["You must pass in at least two streams of data"]},
        )

    def test_simple_two_param_or(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/32/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "SELL"},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {"response": [{"timestamp": "01/07/2020", "order": "SELL"}]},
        )

    def test_simple_two_param_or_different_timestamp(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/08/2020", "order": "SELL"},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/08/2020", "order": "SELL"},
                ]
            },
        )

    def test_simple_three_param_or(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-3": [{"timestamp": "01/07/2020", "order": "SELL"}],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {"response": [{"timestamp": "01/07/2020", "order": "SELL"}]},
        )

    def test_buy_same_timestamp_does_not_trigger_intersect(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-3": [{"timestamp": "01/07/2020", "order": "BUY"}],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(response.json(), {"response": []})

    def test_buy_multiple_timestamp_trigger_multiple_intersect(self):
        payload = {
            "input": {"event_action": "BUY"},
            "output": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-3": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/23/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/5/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                    {"timestamp": "01/23/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ]
            },
        )
