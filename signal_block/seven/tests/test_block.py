from django.test import TestCase

from blocks.event import event_ingestor
from signal_block.seven.exceptions import (
    SignalBlockSevenInputBlockOneInvalidDataStringException,
    SignalBlockSevenInputBlockOneMissingDataFieldException,
    SignalBlockSevenInputBlockTwoInvalidDataStringException,
    SignalBlockSevenInputBlockTwoMissingDataFieldException,
    SignalBlockSevenInvalidComparisonTypeException,
    SignalBlockSevenInvalidInputPayloadException,
    SignalBlockSevenMissingInputBlockOneException,
    SignalBlockSevenMissingInputBlockTwoException,
)

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


class TriggerEvent(TestCase):
    def test_success_json_less_than_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-volume",
                "incoming_data_two": "2-data",
                "comparison_type": "<",
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
                ],
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_success_json_less_than_equal_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-volume",
                "incoming_data_two": "2-data",
                "comparison_type": "<=",
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
                ],
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                ]
            },
        )

    def test_success_json_more_than_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-volume",
                "incoming_data_two": "2-data",
                "comparison_type": ">",
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
                ],
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_success_json_more_than_equal_buy(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-volume",
                "incoming_data_two": "2-data",
                "comparison_type": ">=",
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
                ],
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ]
            },
        )

    def test_success_json_more_than_equal_buy_both_computational_block(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-data",
                "incoming_data_two": "2-data",
                "comparison_type": ">=",
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
                ],
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

    def test_success_json_more_than_equal_buy_custom_blocks(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-value",
                "incoming_data_two": "2-field",
                "comparison_type": ">=",
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
                ],
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

    def test_failure_missing_input(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_two": "2-field",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInvalidInputPayloadException):
            event_ingestor(payload)

    def test_failure_missing_input_block_one(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "3-value",
                "incoming_data_two": "2-field",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenMissingInputBlockOneException):
            event_ingestor(payload)

    def test_failure_missing_input_block_two(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-value",
                "incoming_data_two": "3-field",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenMissingInputBlockTwoException):
            event_ingestor(payload)

    def test_failure_missing_field_info_from_incoming_data_one(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1",
                "incoming_data_two": "2-field",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInputBlockOneInvalidDataStringException):
            event_ingestor(payload)

    def test_failure_missing_field_info_from_incoming_data_two(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-value",
                "incoming_data_two": "2",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInputBlockTwoInvalidDataStringException):
            event_ingestor(payload)

    def test_failure_field_dne_incoming_data_one(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-foo",
                "incoming_data_two": "2-field",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInputBlockOneMissingDataFieldException):
            event_ingestor(payload)

    def test_failure_field_dne_incoming_data_two(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-value",
                "incoming_data_two": "2-foo",
                "comparison_type": ">=",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInputBlockTwoMissingDataFieldException):
            event_ingestor(payload)

    def test_failure_invalid_comparison_type(self):
        payload = {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
            "inputs": {
                "incoming_data_one": "1-value",
                "incoming_data_two": "2-field",
                "comparison_type": "FOO",
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
                ],
            },
        }

        with self.assertRaises(SignalBlockSevenInvalidComparisonTypeException):
            event_ingestor(payload)
