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

POWER_DATA_BLOCK = [
    {
        "timestamp": "01/01/2020",
        "timezone": "UTC/EST",
        "open": "100.00",
        "high": "100.00",
        "low": "100.00",
        "close": "100.00",
        "volume": "100.00",
    },
    {
        "timestamp": "01/02/2020",
        "timezone": "UTC/EST",
        "open": "1000.00",
        "high": "1000.00",
        "low": "1000.00",
        "close": "1000.00",
        "volume": "1000.00",
    },
    {
        "timestamp": "01/03/2020",
        "timezone": "UTC/EST",
        "open": "10000.00",
        "high": "10000.00",
        "low": "10000.00",
        "close": "10000.00",
        "volume": "10000.00",
    },
    {
        "timestamp": "01/04/2020",
        "timezone": "UTC/EST",
        "open": "100000.00",
        "high": "100000.00",
        "low": "100000.00",
        "close": "100000.00",
        "volume": "100000.00",
    },
    {
        "timestamp": "01/05/2020",
        "timezone": "UTC/EST",
        "open": "1000000.00",
        "high": "1000000.00",
        "low": "1000000.00",
        "close": "1000000.00",
        "volume": "1000000.00",
    },
]


class TriggerEvent(TestCase):
    def test_success_json_add(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "+",
                "operation_value": "5",
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
                    {"timestamp": "01/01/2020", "data": 15.0},
                    {"timestamp": "01/02/2020", "data": 16.0},
                    {"timestamp": "01/03/2020", "data": 17.0},
                    {"timestamp": "01/04/2020", "data": 18.0},
                    {"timestamp": "01/05/2020", "data": 19.0},
                ]
            },
        )

    def test_success_json_add_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "+",
                "operation_value": "-5",
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
                    {"timestamp": "01/01/2020", "data": 5.0},
                    {"timestamp": "01/02/2020", "data": 6.0},
                    {"timestamp": "01/03/2020", "data": 7.0},
                    {"timestamp": "01/04/2020", "data": 8.0},
                    {"timestamp": "01/05/2020", "data": 9.0},
                ]
            },
        )

    def test_success_json_add_decimal(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "+",
                "operation_value": "0.5",
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
                    {"timestamp": "01/01/2020", "data": 10.5},
                    {"timestamp": "01/02/2020", "data": 11.5},
                    {"timestamp": "01/03/2020", "data": 12.5},
                    {"timestamp": "01/04/2020", "data": 13.5},
                    {"timestamp": "01/05/2020", "data": 14.5},
                ]
            },
        )

    def test_success_json_subtract(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "-",
                "operation_value": "5",
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
                    {"timestamp": "01/01/2020", "data": 5.0},
                    {"timestamp": "01/02/2020", "data": 6.0},
                    {"timestamp": "01/03/2020", "data": 7.0},
                    {"timestamp": "01/04/2020", "data": 8.0},
                    {"timestamp": "01/05/2020", "data": 9.0},
                ]
            },
        )

    def test_success_json_subtract_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "-",
                "operation_value": "-5",
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
                    {"timestamp": "01/01/2020", "data": 15.0},
                    {"timestamp": "01/02/2020", "data": 16.0},
                    {"timestamp": "01/03/2020", "data": 17.0},
                    {"timestamp": "01/04/2020", "data": 18.0},
                    {"timestamp": "01/05/2020", "data": 19.0},
                ]
            },
        )

    def test_success_json_subtract_decimal(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "-",
                "operation_value": "-0.5",
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
                    {"timestamp": "01/01/2020", "data": 10.5},
                    {"timestamp": "01/02/2020", "data": 11.5},
                    {"timestamp": "01/03/2020", "data": 12.5},
                    {"timestamp": "01/04/2020", "data": 13.5},
                    {"timestamp": "01/05/2020", "data": 14.5},
                ]
            },
        )

    def test_success_json_multiply(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "*",
                "operation_value": "5",
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
                    {"timestamp": "01/01/2020", "data": 50.0},
                    {"timestamp": "01/02/2020", "data": 55.0},
                    {"timestamp": "01/03/2020", "data": 60.0},
                    {"timestamp": "01/04/2020", "data": 65.0},
                    {"timestamp": "01/05/2020", "data": 70.0},
                ]
            },
        )

    def test_success_json_multiply_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "*",
                "operation_value": "-5",
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
                    {"timestamp": "01/01/2020", "data": -50.0},
                    {"timestamp": "01/02/2020", "data": -55.0},
                    {"timestamp": "01/03/2020", "data": -60.0},
                    {"timestamp": "01/04/2020", "data": -65.0},
                    {"timestamp": "01/05/2020", "data": -70.0},
                ]
            },
        )

    def test_success_json_multiply_decimal(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "*",
                "operation_value": "0.5",
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
                    {"timestamp": "01/01/2020", "data": 5},
                    {"timestamp": "01/02/2020", "data": 5.5},
                    {"timestamp": "01/03/2020", "data": 6},
                    {"timestamp": "01/04/2020", "data": 6.5},
                    {"timestamp": "01/05/2020", "data": 7},
                ]
            },
        )

    def test_success_json_divide(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "/",
                "operation_value": "5",
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
                    {"timestamp": "01/01/2020", "data": 2},
                    {"timestamp": "01/02/2020", "data": 2.2},
                    {"timestamp": "01/03/2020", "data": 2.4},
                    {"timestamp": "01/04/2020", "data": 2.6},
                    {"timestamp": "01/05/2020", "data": 2.8},
                ]
            },
        )

    def test_success_json_divide_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "/",
                "operation_value": "-5",
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
                    {"timestamp": "01/01/2020", "data": -2},
                    {"timestamp": "01/02/2020", "data": -2.2},
                    {"timestamp": "01/03/2020", "data": -2.4},
                    {"timestamp": "01/04/2020", "data": -2.6},
                    {"timestamp": "01/05/2020", "data": -2.8},
                ]
            },
        )

    def test_success_json_divide_decimal(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "/",
                "operation_value": "0.5",
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
                    {"timestamp": "01/01/2020", "data": 20},
                    {"timestamp": "01/02/2020", "data": 22},
                    {"timestamp": "01/03/2020", "data": 24},
                    {"timestamp": "01/04/2020", "data": 26},
                    {"timestamp": "01/05/2020", "data": 28},
                ]
            },
        )

    def test_success_json_power(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "^",
                "operation_value": "2",
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
                    {"timestamp": "01/01/2020", "data": 100},
                    {"timestamp": "01/02/2020", "data": 121},
                    {"timestamp": "01/03/2020", "data": 144},
                    {"timestamp": "01/04/2020", "data": 169},
                    {"timestamp": "01/05/2020", "data": 196},
                ]
            },
        )

    def test_success_json_power_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "^",
                "operation_value": "2",
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
                    {"timestamp": "01/01/2020", "data": 100},
                    {"timestamp": "01/02/2020", "data": 121},
                    {"timestamp": "01/03/2020", "data": 144},
                    {"timestamp": "01/04/2020", "data": 169},
                    {"timestamp": "01/05/2020", "data": 196},
                ]
            },
        )

    def test_success_json_power_negative(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "close",
                "operation_type": "^",
                "operation_value": "-1",
            },
            "outputs": {
                "DATA_BLOCK-1-1": POWER_DATA_BLOCK,
            },
        }
        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": 0.01},
                    {"timestamp": "01/02/2020", "data": 0.001},
                    {"timestamp": "01/03/2020", "data": 0.0001},
                    {"timestamp": "01/04/2020", "data": 0.00001},
                    {"timestamp": "01/05/2020", "data": 0.000001},
                ]
            },
        )

    def test_success_json_multiply_volume(self):
        payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
            "inputs": {
                "data_field": "volume",
                "operation_type": "*",
                "operation_value": "5",
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
                    {"timestamp": "01/01/2020", "data": 50.0},
                    {"timestamp": "01/02/2020", "data": 55.0},
                    {"timestamp": "01/03/2020", "data": 60.0},
                    {"timestamp": "01/04/2020", "data": 65.0},
                    {"timestamp": "01/05/2020", "data": 70.0},
                ]
            },
        )

    # TODO: Test for only 1 input dataset
    # TODO: Test for only numbers in operation_value
    # def test_failure_json_more_than_one_data(self):
    #     payload = {
    #         "blockType": "COMPUTATIONAL_BLOCK",
    #         "blockId": 2,
    #         "inputs": {
    #             "data_field": "close",
    #             "operation_type": "+",
    #             "operation_value": "5",
    #         },
    #         "outputs": {
    #             "DATA_BLOCK-1-1": POWER_DATA_BLOCK,
    #             "DATA_BLOCK-1-2": POWER_DATA_BLOCK,
    #         },
    #     }
    #     response = event_ingestor(payload)
    #     self.assertDictEqual(
    #         response,
    #         {
    #             "response": "..."
    #         },
    #     )
