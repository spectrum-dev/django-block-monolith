import json

from django.test import TestCase


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/1/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class PostRun(TestCase):
    def test_intersect_event_two_outputs_single_intersection_ok(self):
        payload = {
            "input": {"event_action": "BUY"},
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "2020-01-01", "data": 14.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 10.00},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/1/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(), {"response": [{"timestamp": "2020-01-02", "order": "BUY"}]}
        )

    def test_intersect_event_two_outputs_single_intersection_ok(self):
        payload = {
            "input": {"event_action": "BUY"},
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 9.00},
                    {"timestamp": "2020-01-5", "data": 7.00},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "2020-01-01", "data": 14.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 10.00},
                    {"timestamp": "2020-01-04", "data": 9.00},
                    {"timestamp": "2020-01-5", "data": 7.00},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/1/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "2020-01-02", "order": "BUY"},
                    {"order": "BUY", "timestamp": "2020-01-04"},
                ]
            },
        )

    def test_intersect_event_three_outputs_single_intersection_ok(self):
        payload = {
            "input": {"event_action": "SELL"},
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 12.00},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "2020-01-01", "data": 14.00},
                    {"timestamp": "2020-01-02", "data": 13.50},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 12.00},
                ],
                "COMPUTATIONAL_BLOCK-1-3": [
                    {"timestamp": "2020-01-01", "data": 9.00},
                    {"timestamp": "2020-01-02", "data": 10.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 15.00},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/1/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {"response": [{"timestamp": "2020-01-03", "order": "SELL"}]},
        )

    def test_less_than_two_output_streams_error(self):
        payload = {
            "input": {"event_action": "BUY"},
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/1/run", json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "You must pass in at least two different streams of data"
                ]
            },
        )