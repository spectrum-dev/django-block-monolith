from django.test import TestCase

from blocks.event import event_ingestor


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/1/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class PostRun(TestCase):
    def setUp(self):
        self.payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
        }

    def test_intersect_event_two_outputs_single_intersection_ok(self):
        payload = {
            **self.payload,
            "inputs": {"event_action": "BUY"},
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(response, [{"timestamp": "2020-01-02", "order": "BUY"}])

    def test_intersect_event_two_outputs_single_intersection_ok(self):
        payload = {
            **self.payload,
            "inputs": {"event_action": "BUY"},
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-02", "order": "BUY"},
                {"order": "BUY", "timestamp": "2020-01-04"},
            ],
        )

    def test_intersect_event_three_outputs_single_intersection_ok(self):
        payload = {
            **self.payload,
            "inputs": {"event_action": "SELL"},
            "outputs": {
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

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [{"timestamp": "2020-01-03", "order": "SELL"}],
        )
