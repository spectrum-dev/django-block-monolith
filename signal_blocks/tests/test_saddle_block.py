import json

from django.test import TestCase


class GetSaddleType(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/2/saddleType")

        self.assertEqual(response.json(), {"response": ["DOWNWARD", "UPWARD"]})


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/2/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class PostRun(TestCase):
    def test_upward_ok(self):
        payload = {
            "input": {
                "saddle_type": "UPWARD",
                "event_action": "BUY",
                "consecutive_up": 2,
                "consecutive_down": 1,
            },
            "output": {
                "DATA_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 16.00},
                    {"timestamp": "2020-01-05", "data": 15.00},
                    {"timestamp": "2020-01-06", "data": 20.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(), {"response": [{"timestamp": "2020-01-06", "order": "BUY"}]}
        )

    def test_upward_no_event(self):
        payload = {
            "input": {
                "saddle_type": "UPWARD",
                "event_action": "BUY",
                "consecutive_up": 2,
                "consecutive_down": 1,
            },
            "output": {
                "DATA_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 14.00},
                    {"timestamp": "2020-01-05", "data": 15.00},
                    {"timestamp": "2020-01-06", "data": 27.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(response.json(), {"response": []})

    def test_downward_ok(self):
        payload = {
            "input": {
                "saddle_type": "DOWNWARD",
                "event_action": "BUY",
                "consecutive_down": 2,
                "consecutive_up": 1,
            },
            "output": {
                "DATA_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 8.00},
                    {"timestamp": "2020-01-03", "data": 6.00},
                    {"timestamp": "2020-01-04", "data": 9.00},
                    {"timestamp": "2020-01-05", "data": 4.00},
                    {"timestamp": "2020-01-06", "data": 2.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(), {"response": [{"order": "BUY", "timestamp": "2020-01-05"}]}
        )

    def test_downward_no_event(self):
        payload = {
            "input": {
                "saddle_type": "DOWNWARD",
                "event_action": "BUY",
                "consecutive_down": 2,
                "consecutive_up": 1,
            },
            "output": {
                "DATA_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 9.00},
                    {"timestamp": "2020-01-03", "data": 8.00},
                    {"timestamp": "2020-01-04", "data": 7.00},
                    {"timestamp": "2020-01-05", "data": 6.00},
                    {"timestamp": "2020-01-06", "data": 5.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/2/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(response.json(), {"response": []})
