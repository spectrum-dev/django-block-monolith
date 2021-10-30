from django.test.testcases import TestCase

from blocks.event import event_ingestor


class TestOrRun(TestCase):
    def setUp(self):
        self.payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 5,
        }

    def test_simple_two_param_or_with_buy_and_sell_conflict(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "SELL"},
                ],
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/31/2020", "order": "BUY"},
            ],
        )

    def test_simple_two_param_or_different_timestamp(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/02/2020", "order": "SELL"},
                {"timestamp": "01/07/2020", "order": "BUY"},
                {"timestamp": "01/08/2020", "order": "SELL"},
                {"timestamp": "01/31/2020", "order": "BUY"},
            ],
        )

    def test_one_input_empty(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [],
                "SIGNAL_BLOCK-1-3": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "SELL"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                ],
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/07/2020", "order": "BUY"},
                {"timestamp": "01/14/2020", "order": "SELL"},
                {"timestamp": "01/21/2020", "order": "BUY"},
                {"timestamp": "01/31/2020", "order": "BUY"},
            ],
        )

    def test_simple_three_param_or(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-3": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "BUY"},
                    {"timestamp": "01/14/2020", "order": "BUY"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                ],
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/07/2020", "order": "BUY"},
                {"timestamp": "01/14/2020", "order": "BUY"},
                {"timestamp": "01/21/2020", "order": "BUY"},
            ],
        )

    def test_buy_sell_same_timestamp_does_not_trigger_intersect(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/07/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "SELL"},
                ],
                "SIGNAL_BLOCK-1-3": [{"timestamp": "01/07/2020", "order": "SELL"}],
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(response, [])

    def test_multiple_timestamp_trigger_multiple_intersect(self):
        payload = {
            **self.payload,
            "inputs": {},
            "outputs": {
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/21/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-2": [
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/14/2020", "order": "SELL"},
                    {"timestamp": "01/31/2020", "order": "BUY"},
                ],
                "SIGNAL_BLOCK-1-3": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/07/2020", "order": "SELL"},
                    {"timestamp": "01/23/2020", "order": "BUY"},
                    {"timestamp": "01/31/2020", "order": "SELL"},
                ],
            },
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/07/2020", "order": "SELL"},
                {"timestamp": "01/14/2020", "order": "SELL"},
                {"timestamp": "01/21/2020", "order": "BUY"},
                {"timestamp": "01/23/2020", "order": "BUY"},
            ],
        )
