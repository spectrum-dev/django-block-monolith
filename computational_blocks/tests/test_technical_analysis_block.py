import json
from django.test import TestCase

from computational_blocks.blocks.technical_analysis.main import run
from computational_blocks.tests.data.technical_analysis import DATA_BLOCK


class GetIndicator(TestCase):
    def test_ok(self):
        response = self.client.get(f"/COMPUTATIONAL_BLOCK/1/indicator")

        self.assertEqual(
            response.json(),
            {
                "response": [
                    "MA",
                    "EMA",
                    "MACD",
                    "ADX",
                    "ADXR",
                    "APO",
                    "AROONOSC",
                    "BOP",
                    "CCI",
                    "CMO",
                    "DX",
                    "RSI",
                ]
            },
        )


class GetIndicatorField(TestCase):
    def test_ok(self):
        indicator_name = "MA"
        response = self.client.get(
            f"/COMPUTATIONAL_BLOCK/1/indicatorField?indicatorName={indicator_name}"
        )

        self.assertEqual(
            response.json(),
            {
                "response": [
                    {
                        "fieldName": "Incoming Data",
                        "fieldVariableName": "incoming_data",
                        "fieldType": "inputs_from_connection",
                        "fieldDefaultValue": "close",
                    },
                    {
                        "fieldName": "Lookback Period",
                        "fieldVariableName": "lookback_period",
                        "fieldType": "input",
                    },
                ]
            },
        )

    def test_error_not_found(self):
        indicator_name = "INDICATOR_DNE"
        response = self.client.get(
            f"/COMPUTATIONAL_BLOCK/1/indicatorField?indicatorName={indicator_name}"
        )

        self.assertEqual(
            response.json(), {"error": "The indicator INDICATOR_DNE was not found"}
        )


class PostRun(TestCase):
    def test_compute_ma(self):
        payload = {
            "input": {
                "indicator_name": "MA",
                "lookback_period": "2",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": 10.5},
                    {"timestamp": "01/03/2020", "data": 12.0},
                    {"timestamp": "01/04/2020", "data": 12.5},
                    {"timestamp": "01/05/2020", "data": 13.0},
                ]
            },
        )

    def test_compute_ema(self):
        payload = {
            "input": {
                "indicator_name": "EMA",
                "lookback_period": "2",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": 10.5},
                    {"timestamp": "01/03/2020", "data": 12.1666666667},
                    {"timestamp": "01/04/2020", "data": 12.0555555556},
                    {"timestamp": "01/05/2020", "data": 13.3518518519},
                ]
            },
        )

    def test_compute_macd(self):
        payload = {
            "input": {
                "indicator_name": "MACD",
                "lookback_period_one": "2",
                "lookback_period_two": "3",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": 0.8333333333},
                    {"timestamp": "01/04/2020", "data": 0.3888888889},
                    {"timestamp": "01/05/2020", "data": 0.5185185185},
                ]
            },
        )

    def test_compute_adx(self):
        payload = {
            "input": {
                "indicator_name": "ADX",
                "lookback_period": "2",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 55.5555555556},
                    {"timestamp": "01/05/2020", "data": 61.7777777778},
                ]
            },
        )

    def test_compute_adxr(self):
        payload = {
            "input": {
                "indicator_name": "ADXR",
                "lookback_period": "2",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": None},
                    {"timestamp": "01/05/2020", "data": 58.6666666667},
                ]
            },
        )

    def test_compute_apo(self):
        payload = {
            "input": {
                "indicator_name": "APO",
                "fast_period": "2",
                "slow_period": "4",
                "ma_type": "0",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 1.0},
                    {"timestamp": "01/05/2020", "data": 0.5},
                ]
            },
        )

    def test_compute_aroon_oscillator(self):
        payload = {
            "input": {
                "indicator_name": "AROONOSC",
                "lookback_period": 3,
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 66.6666666667},
                    {"timestamp": "01/05/2020", "data": 100.0},
                ]
            },
        )

    def test_compute_bop(self):
        payload = {
            "input": {
                "indicator_name": "BOP",
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": 0.0},
                    {"timestamp": "01/02/2020", "data": 0.0},
                    {"timestamp": "01/03/2020", "data": 0.0},
                    {"timestamp": "01/04/2020", "data": 0.0},
                    {"timestamp": "01/05/2020", "data": 0.0},
                ]
            },
        )

    def test_compute_cci(self):
        payload = {
            "input": {
                "indicator_name": "CCI",
                "lookback_period": 3,
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": 100.0},
                    {"timestamp": "01/04/2020", "data": 0.0},
                    {"timestamp": "01/05/2020", "data": 100.0},
                ]
            },
        )

    def test_compute_cmo(self):
        payload = {
            "input": {
                "indicator_name": "CMO",
                "lookback_period": 3,
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 50.0},
                    {"timestamp": "01/05/2020", "data": 71.4285714286},
                ]
            },
        )

    def test_compute_dx(self):
        payload = {
            "input": {
                "indicator_name": "DX",
                "lookback_period": 3,
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 33.3333333333},
                    {"timestamp": "01/05/2020", "data": 66.6666666667},
                ]
            },
        )

    def test_compute_rsi(self):
        payload = {
            "input": {
                "indicator_name": "RSI",
                "lookback_period": 3,
            },
            "output": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = self.client.post(
            "/COMPUTATIONAL_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": None},
                    {"timestamp": "01/03/2020", "data": None},
                    {"timestamp": "01/04/2020", "data": 100.0},
                    {"timestamp": "01/05/2020", "data": 100.0},
                ]
            },
        )
