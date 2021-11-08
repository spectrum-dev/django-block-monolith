from django.test import TestCase

from blocks.event import event_ingestor
from signal_block.six.exceptions import (
    SignalBlockSixInvalidEventTypeException,
    SignalBlockSixInvalidInputPayloadException,
)
from signal_block.six.tests.fixture import DATA_BLOCK, DATA_BLOCK_2


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

    def test_missing_input(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK_2,
            },
        }

        with self.assertRaises(SignalBlockSixInvalidInputPayloadException):
            event_ingestor(payload)

    def test_invalid_event_action(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "FOO",
                "event_type": "CLOSE_ABOVE_OPEN",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK_2,
            },
        }

        with self.assertRaises(SignalBlockSixInvalidInputPayloadException):
            event_ingestor(payload)

    def test_invalid_event_type(self):
        payload = {
            **self.payload,
            "inputs": {
                "event_action": "BUY",
                "event_type": "FOO",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK_2,
            },
        }

        with self.assertRaises(SignalBlockSixInvalidEventTypeException):
            event_ingestor(payload)
