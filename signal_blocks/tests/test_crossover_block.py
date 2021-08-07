import json

from django.test import TestCase


class GetCrossoverType(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/4/crossoverType")

        self.assertEqual(response.json(), {"response": ["ABOVE", "BELOW"]})


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/4/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class PostRun(TestCase):
    def test_crossover_above_event_single_action_ok(self):
        payload = {
            "input": {
                "event_type": "ABOVE",
                "event_action": "BUY",
                "event_value": "15",
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 16.00},
                    {"timestamp": "2020-01-05", "data": 17.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/4/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(), {"response": [{"timestamp": "2020-01-04", "order": "BUY"}]}
        )

    def test_crossover_below_event_single_action_ok(self):
        payload = {
            "input": {
                "event_type": "BELOW",
                "event_action": "SELL",
                "event_value": "15",
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 13.00},
                    {"timestamp": "2020-01-03", "data": 25.00},
                    {"timestamp": "2020-01-04", "data": 20.00},
                    {"timestamp": "2020-01-05", "data": 10.00},
                    {"timestamp": "2020-01-06", "data": 8.00},
                    {"timestamp": "2020-01-07", "data": 4.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/4/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {"response": [{"timestamp": "2020-01-05", "order": "SELL"}]},
        )

    def test_crossover_below_event_multiple_actions_ok(self):
        payload = {
            "input": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "event_value": "15",
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 20.00},
                    {"timestamp": "2020-01-02", "data": 15.00},
                    {"timestamp": "2020-01-03", "data": 10.00},
                    {"timestamp": "2020-01-04", "data": 13.00},
                    {"timestamp": "2020-01-05", "data": 35.00},
                    {"timestamp": "2020-01-06", "data": 42.00},
                    {"timestamp": "2020-01-07", "data": 22.00},
                    {"timestamp": "2020-01-08", "data": 8.00},
                    {"timestamp": "2020-01-09", "data": 20.00},
                    {"timestamp": "2020-01-10", "data": 13.00},
                    {"timestamp": "2020-01-11", "data": 25.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/4/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "2020-01-03", "order": "BUY"},
                    {"timestamp": "2020-01-08", "order": "BUY"},
                    {"timestamp": "2020-01-10", "order": "BUY"},
                ]
            },
        )

    def test_crossover_below_begin_below_threshold_ok(self):
        payload = {
            "input": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "event_value": "15",
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 10.00},
                    {"timestamp": "2020-01-03", "data": 10.00},
                    {"timestamp": "2020-01-04", "data": 21.00},
                    {"timestamp": "2020-01-05", "data": 35.00},
                    {"timestamp": "2020-01-06", "data": 42.00},
                    {"timestamp": "2020-01-07", "data": 10.00},
                    {"timestamp": "2020-01-08", "data": 8.00},
                ]
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/4/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "2020-01-07", "order": "BUY"},
                ]
            },
        )

    def test_more_than_one_output_stream_data_error(self):
        payload = {
            "input": {
                "event_type": "ABOVE",
                "event_action": "BUY",
                "event_value": "15",
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                ],
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/4/run", json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(
            response.json(),
            {"non_field_errors": ["You must pass in at most one stream of data"]},
        )
