import json
from django.test import TestCase

from computational_blocks.blocks.technical_analysis.main import run
from signal_blocks.tests.data.data_block import DATA_BLOCK


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get(f"/SIGNAL_BLOCK/6/eventAction")

        self.assertEqual(
            response.json(),
            {
                "response": [
                    "BUY",
                    "SELL",
                ]
            },
        )


class GetEventType(TestCase):
    def test_ok(self):
        response = self.client.get(f"/SIGNAL_BLOCK/6/candleCloseType")

        self.assertEqual(
            response.json(),
            {
                "response": [
                    "CLOSE_ABOVE_OPEN",
                    "CLOSE_BELOW_OPEN",
                    "CLOSE_EQ_HIGH",
                    "CLOSE_BELOW_HIGH",
                    "CLOSE_ABOVE_LOW",
                    "CLOSE_EQ_LOW",
                ]
            },
        )


class PostRun(TestCase):
    def test_more_than_one_output_stream_data_error(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK, "DATA_BLOCK-1-2": DATA_BLOCK},
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {"non_field_errors": ["You must pass in at most one stream of data"]},
        )

    def test_close_above_low(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_LOW",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_above_open(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_below_high(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_BELOW_HIGH",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_below_open(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_BELOW_OPEN",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_high(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_EQ_HIGH",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_low(self):
        payload = {
            "input": {
                "event_action": "BUY",
                "event_type": "CLOSE_EQ_LOW",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_low_sell(self):
        payload = {
            "input": {
                "event_action": "SELL",
                "event_type": "CLOSE_EQ_LOW",
            },
            "output": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = self.client.post(
            "/SIGNAL_BLOCK/6/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/03/2020", "order": "SELL"},
                    {"timestamp": "01/05/2020", "order": "SELL"},
                ]
            },
        )
