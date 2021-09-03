import json

from django.test import TestCase
from blocks.event import event_ingestor

DATA_BLOCK = [
    {
        "timestamp": "01/01/2020",
        "timezone": "UTC/EST",
        "open": "10.00",
        "high": "10.00",
        "low": "10.00",
        "close": "10.00",
        "volume": "10.00",
    },
    {
        "timestamp": "01/02/2020",
        "timezone": "UTC/EST",
        "open": "11.00",
        "high": "11.00",
        "low": "11.00",
        "close": "11.00",
        "volume": "11.00",
    },
    {
        "timestamp": "01/03/2020",
        "timezone": "UTC/EST",
        "open": "12.00",
        "high": "12.00",
        "low": "12.00",
        "close": "12.00",
        "volume": "12.00",
    },
    {
        "timestamp": "01/04/2020",
        "timezone": "UTC/EST",
        "open": "13.00",
        "high": "13.00",
        "low": "13.00",
        "close": "13.00",
        "volume": "13.00",
    },
    {
        "timestamp": "01/05/2020",
        "timezone": "UTC/EST",
        "open": "14.00",
        "high": "14.00",
        "low": "14.00",
        "close": "14.00",
        "volume": "14.00",
    },
]

class GetComparisonType(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/7/comparisonType")

        self.assertEqual(
            response.json(),
            {
                "response": [
                    "LESS_THAN",
                    "LESS_THAN_EQUAL",
                    "MORE_THAN",
                    "MORE_THAN_EQUAL",
                ]
            },
        )


class GetEventAction(TestCase):
    def test_ok(self):
        response = self.client.get("/SIGNAL_BLOCK/7/eventAction")

        self.assertEqual(response.json(), {"response": ["BUY", "SELL"]})


class TriggerEvent(TestCase):
    
    def test_success_json_less_than_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "DATA_BLOCK-1-1",
                "input_block_1_field": "volume",
                "comparison_type": "LESS_THAN",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "data",
                "event_action": "BUY",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "data": "12.00"},
                    {"timestamp": "01/02/2020", "data": "12.00"},
                    {"timestamp": "01/03/2020", "data": "12.00"},
                    {"timestamp": "01/04/2020", "data": "12.00"},
                    {"timestamp": "01/05/2020", "data": "15.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/01/2020", "order": "BUY"},
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/05/2020", "order": "BUY"},
            ]
        })

    def test_success_json_less_than_equal_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "DATA_BLOCK-1-1",
                "input_block_1_field": "volume",
                "comparison_type": "LESS_THAN_EQUAL",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "data",
                "event_action": "BUY",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "data": "12.00"},
                    {"timestamp": "01/02/2020", "data": "12.00"},
                    {"timestamp": "01/03/2020", "data": "12.00"},
                    {"timestamp": "01/04/2020", "data": "12.00"},
                    {"timestamp": "01/05/2020", "data": "15.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/01/2020", "order": "BUY"},
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/03/2020", "order": "BUY"},
                {"timestamp": "01/05/2020", "order": "BUY"},
            ]
        })
    
    def test_success_json_more_than_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "DATA_BLOCK-1-1",
                "input_block_1_field": "volume",
                "comparison_type": "MORE_THAN",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "data",
                "event_action": "BUY",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "data": "12.00"},
                    {"timestamp": "01/02/2020", "data": "12.00"},
                    {"timestamp": "01/03/2020", "data": "12.00"},
                    {"timestamp": "01/04/2020", "data": "12.00"},
                    {"timestamp": "01/05/2020", "data": "15.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/04/2020", "order": "BUY"},
            ]
        })

    def test_success_json_more_than_equal_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "DATA_BLOCK-1-1",
                "input_block_1_field": "volume",
                "comparison_type": "MORE_THAN_EQUAL",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "data",
                "event_action": "BUY",
            },
            "outputs": {
                "DATA_BLOCK-1-1": DATA_BLOCK,
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "data": "12.00"},
                    {"timestamp": "01/02/2020", "data": "12.00"},
                    {"timestamp": "01/03/2020", "data": "12.00"},
                    {"timestamp": "01/04/2020", "data": "12.00"},
                    {"timestamp": "01/05/2020", "data": "15.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/03/2020", "order": "BUY"},
                {"timestamp": "01/04/2020", "order": "BUY"},
            ]
        })
    
    def test_success_json_more_than_equal_buy_both_computational_block(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "COMPUTATIONAL_BLOCK-1-1",
                "input_block_1_field": "data",
                "comparison_type": "MORE_THAN_EQUAL",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "data",
                "event_action": "BUY",
            },
            "outputs": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "01/01/2020", "data": "13.00"},
                    {"timestamp": "01/02/2020", "data": "13.00"},
                    {"timestamp": "01/03/2020", "data": "7.00"},
                    {"timestamp": "01/04/2020", "data": "19.00"},
                    {"timestamp": "01/05/2020", "data": "20.00"},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "data": "12.00"},
                    {"timestamp": "01/02/2020", "data": "12.00"},
                    {"timestamp": "01/03/2020", "data": "12.00"},
                    {"timestamp": "01/04/2020", "data": "12.00"},
                    {"timestamp": "01/05/2020", "data": "21.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/01/2020", "order": "BUY"},
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/04/2020", "order": "BUY"},
            ]
        })
    
    def test_success_json_more_than_equal_buy_custom_blocks(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "input_block_1_name": "COMPUTATIONAL_BLOCK-1-1",
                "input_block_1_field": "value",
                "comparison_type": "MORE_THAN_EQUAL",
                "input_block_2_name": "COMPUTATIONAL_BLOCK-1-2",
                "input_block_2_field": "field",
                "event_action": "BUY",
            },
            "outputs": {
                "COMPUTATIONAL_BLOCK-1-1": [
                    {"timestamp": "01/01/2020", "value": "13.00"},
                    {"timestamp": "01/02/2020", "value": "13.00"},
                    {"timestamp": "01/03/2020", "value": "7.00"},
                    {"timestamp": "01/04/2020", "value": "19.00"},
                    {"timestamp": "01/05/2020", "value": "20.00"},
                ],
                "COMPUTATIONAL_BLOCK-1-2": [
                    {"timestamp": "01/01/2020", "field": "12.00"},
                    {"timestamp": "01/02/2020", "field": "12.00"},
                    {"timestamp": "01/03/2020", "field": "12.00"},
                    {"timestamp": "01/04/2020", "field": "12.00"},
                    {"timestamp": "01/05/2020", "field": "21.00"},
                ]
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(response, {
            "response": [
                {"timestamp": "01/01/2020", "order": "BUY"},
                {"timestamp": "01/02/2020", "order": "BUY"},
                {"timestamp": "01/04/2020", "order": "BUY"},
            ]
        })