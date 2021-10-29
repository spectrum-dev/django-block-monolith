import json
from django.test import TestCase

from signal_blocks.tests.data.data_block import DATA_BLOCK, DATA_BLOCK_2

from blocks.event import event_ingestor


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
    def setUp(self):
        self.payload = {"blockType": "SIGNAL_BLOCK", "blockId": 6}

    def test_close_above_low(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_LOW",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
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
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_below_high(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_BELOW_HIGH",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
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
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_BELOW_OPEN",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_high(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_EQ_HIGH",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_low(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_EQ_LOW",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_close_eq_low_sell(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "SELL",
                "event_type": "CLOSE_EQ_LOW",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/03/2020", "order": "SELL"},
                    {"timestamp": "01/05/2020", "order": "SELL"},
                ]
            },
        )

    def test_no_results(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK_2,
            },
        }

        response = event_ingestor(payload)

        self.assertDictEqual(
            response,
            {"response": []},
        )
