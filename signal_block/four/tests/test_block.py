from django.test import TestCase

from blocks.event import event_ingestor
from signal_block.four.exceptions import SignalBlockFourInvalidInputPayloadException


class PostRun(TestCase):
    def setUp(self):
        self.payload = {"blockType": "SIGNAL_BLOCK", "blockId": 4}

    def test_crossover_above_event_single_action_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "ABOVE",
                "event_action": "BUY",
                "event_value": "15",
                "incoming_data": "1-data",
            },
            "outputs": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "2020-01-01", "data": 10.00},
                    {"timestamp": "2020-01-02", "data": 11.00},
                    {"timestamp": "2020-01-03", "data": 13.00},
                    {"timestamp": "2020-01-04", "data": 16.00},
                    {"timestamp": "2020-01-05", "data": 17.00},
                ]
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(response, [{"timestamp": "2020-01-04", "order": "BUY"}])

    def test_crossover_above_event_single_action_ok_close_field(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "ABOVE",
                "event_action": "BUY",
                "event_value": "15",
                "incoming_data": "3-close",
            },
            "outputs": {
                "COMPUTATIONAL_BLOCK-1-3": [
                    {"timestamp": "2020-01-01", "close": 10.00},
                    {"timestamp": "2020-01-02", "close": 11.00},
                    {"timestamp": "2020-01-03", "close": 13.00},
                    {"timestamp": "2020-01-04", "close": 16.00},
                    {"timestamp": "2020-01-05", "close": 17.00},
                ]
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(response, [{"timestamp": "2020-01-04", "order": "BUY"}])

    def test_crossover_below_event_single_action_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "BELOW",
                "event_action": "SELL",
                "event_value": "15",
                "incoming_data": "1-data",
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [{"timestamp": "2020-01-05", "order": "SELL"}],
        )

    def test_crossover_below_event_multiple_actions_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "event_value": "15",
                "incoming_data": "1-data",
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-03", "order": "BUY"},
                {"timestamp": "2020-01-08", "order": "BUY"},
                {"timestamp": "2020-01-10", "order": "BUY"},
            ],
        )

    def test_crossover_below_begin_below_threshold_ok(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "event_value": "15",
                "incoming_data": "1-data",
            },
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-07", "order": "BUY"},
            ],
        )

    def test_failure_missing_variable(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "incoming_data": "1-data",
            },
            "outputs": {
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

        with self.assertRaises(SignalBlockFourInvalidInputPayloadException):
            event_ingestor(payload)

    def test_failure_event_value_not_castable_to_float(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "BELOW",
                "event_action": "BUY",
                "event_value": "foo",
                "incoming_data": "1-data",
            },
            "outputs": {
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

        with self.assertRaises(SignalBlockFourInvalidInputPayloadException):
            event_ingestor(payload)
