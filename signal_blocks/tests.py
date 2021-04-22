from django.test import TestCase, Client

from signal_blocks.blocks.event_block.main import run
# Create your tests here.

class EventBlock(TestCase):
    def test_intersect_event_two_outputs(self):
        request_payload = {
            "input": {
                "event_type": "INTERSECT",
                "event_action": "BUY"
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {
                        "timestamp": "2020-01-01",
                        "data": 10.00
                    },
                    {
                        "timestamp": "2020-01-02",
                        "data": 11.00
                    },
                    {
                        "timestamp": "2020-01-03",
                        "data": 13.00
                    }
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {
                        "timestamp": "2020-01-01",
                        "data": 14.00
                    },
                    {
                        "timestamp": "2020-01-02",
                        "data": 11.00
                    },
                    {
                        "timestamp": "2020-01-03",
                        "data": 10.00
                    }
                ],
            }
        }

        response = run(request_payload["input"], request_payload["output"])

        assert response == [{'timestamp': '2020-01-02', 'order': 'BUY'}]

    def test_intersect_event_three_outputs(self):
        request_payload = {
            "input": {
                "event_type": "INTERSECT",
                "event_action": "BUY"
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {
                        "timestamp": "2020-01-01",
                        "data": 10.00
                    },
                    {
                        "timestamp": "2020-01-02",
                        "data": 11.00
                    },
                    {
                        "timestamp": "2020-01-03",
                        "data": 13.00
                    },
                    {
                        "timestamp": "2020-01-04",
                        "data": 12.00
                    },
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {
                        "timestamp": "2020-01-01",
                        "data": 14.00
                    },
                    {
                        "timestamp": "2020-01-02",
                        "data": 13.50
                    },
                    {
                        "timestamp": "2020-01-03",
                        "data": 13.00
                    },
                    {
                        "timestamp": "2020-01-04",
                        "data": 12.00
                    },
                ],
                "COMPUTATIONAL_BLOCK-1-3": [
                    {
                        "timestamp": "2020-01-01",
                        "data": 9.00
                    },
                    {
                        "timestamp": "2020-01-02",
                        "data": 10.00
                    },
                    {
                        "timestamp": "2020-01-03",
                        "data": 13.00
                    },
                    {
                        "timestamp": "2020-01-04",
                        "data": 15.00
                    }
                ],
            }
        }

        response = run(request_payload["input"], request_payload["output"])

        assert response == [{'timestamp': '2020-01-03', 'order': 'BUY'}]
