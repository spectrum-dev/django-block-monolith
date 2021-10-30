import json

from django.test import TestCase

from blocks.event import event_ingestor


class GetSaddleType(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/2/saddleType")

        self.assertEqual(response.json(), {"response": ["DOWNWARD", "UPWARD"]})


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/2/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class PostRun(TestCase):
    def setUp(self):
        self.payload = {"blockType": "SIGNAL_BLOCK", "blockId": 2}

    def test_upwards_data_block_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "incoming_data": "close",
                "saddle_type": "UPWARD",
                "event_action": "BUY",
                "consecutive_up": 2,
                "consecutive_down": 1,
            },
            "outputs": {
                "DATA_BLOCK-1-1": [
                    {
                        "timestamp": "2020-01-01",
                        "open": 10.00,
                        "high": 10.00,
                        "low": 10.00,
                        "close": 10.00,
                        "volume": 100.00,
                    },
                    {
                        "timestamp": "2020-01-02",
                        "open": 11.00,
                        "high": 11.00,
                        "low": 11.00,
                        "close": 11.00,
                        "volume": 100.00,
                    },
                    {
                        "timestamp": "2020-01-03",
                        "open": 13.00,
                        "high": 13.00,
                        "low": 13.00,
                        "close": 13.00,
                        "volume": 100.00,
                    },
                    {
                        "timestamp": "2020-01-04",
                        "open": 16.00,
                        "high": 16.00,
                        "low": 16.00,
                        "close": 16.00,
                        "volume": 100.00,
                    },
                    {
                        "timestamp": "2020-01-05",
                        "open": 15.00,
                        "high": 15.00,
                        "low": 15.00,
                        "close": 15.00,
                        "volume": 100.00,
                    },
                    {
                        "timestamp": "2020-01-06",
                        "open": 20.00,
                        "high": 20.00,
                        "low": 20.00,
                        "close": 20.00,
                        "volume": 100.00,
                    },
                ]
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(response, [{"timestamp": "2020-01-06", "order": "BUY"}])

    def test_upward_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "incoming_data": "data",
                "saddle_type": "UPWARD",
                "event_action": "BUY",
                "consecutive_up": 2,
                "consecutive_down": 1,
            },
            "outputs": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 16.00},
                    {"timestamp": "2020-01-05", "data": 15.00},
                    {"timestamp": "2020-01-06", "data": 20.00},
                ]
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(response, [{"timestamp": "2020-01-06", "order": "BUY"}])

    def test_upward_no_event(self):
        payload = {
            **self.payload,
            "inputs": {
                "incoming_data": "data",
                "saddle_type": "UPWARD",
                "event_action": "BUY",
                "consecutive_up": 2,
                "consecutive_down": 1,
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(response, [])

    def test_downward_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "incoming_data": "data",
                "saddle_type": "DOWNWARD",
                "event_action": "BUY",
                "consecutive_down": 2,
                "consecutive_up": 1,
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(response, [{"order": "BUY", "timestamp": "2020-01-05"}])

    def test_downward_no_event(self):
        payload = {
            **self.payload,
            "inputs": {
                "incoming_data": "data",
                "saddle_type": "DOWNWARD",
                "event_action": "BUY",
                "consecutive_down": 2,
                "consecutive_up": 1,
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(response, [])
