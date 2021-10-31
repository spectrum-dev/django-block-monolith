from django.test import TestCase

from blocks.event import event_ingestor

from computational_block.one.tests.fixtures import (
    DATA_BLOCK,
    INTRADAY_DATA_BLOCK,
    INTRADAY_TWO_DAYS_DATA_BLOCK,
)


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
                    "BB",
                    "DB",
                    "KAMA",
                    "KC",
                    "MI",
                    "STOCH_OSCI",
                    "TRIX",
                    "TSI",
                    "OR",
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
    def setUp(self):
        self.payload = {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
        }

    def test_compute_ma(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "MA",
                "lookback_period": "2",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": 10.5},
                {"timestamp": "01/03/2020", "data": 11.5},
                {"timestamp": "01/04/2020", "data": 12.5},
                {"timestamp": "01/05/2020", "data": 13.5},
            ],
        )

    def test_compute_ema(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "EMA",
                "lookback_period": "2",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": 10.5},
                {"timestamp": "01/03/2020", "data": 11.5},
                {"timestamp": "01/04/2020", "data": 12.5},
                {"timestamp": "01/05/2020", "data": 13.5},
            ],
        )

    maxDiff = None

    def test_compute_macd(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "MACD",
                "lookback_period_one": "2",
                "lookback_period_two": "3",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": 0.5},
                {"timestamp": "01/04/2020", "data": 0.5},
                {"timestamp": "01/05/2020", "data": 0.5},
            ],
        )

    def test_compute_adx(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "ADX",
                "lookback_period": "2",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_adxr(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "ADXR",
                "lookback_period": "2",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": None},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_apo(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "APO",
                "fast_period": "2",
                "slow_period": "4",
                "ma_type": "0",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 1.0},
                {"timestamp": "01/05/2020", "data": 1.0},
            ],
        )

    def test_compute_aroon_oscillator(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "AROONOSC",
                "lookback_period": 3,
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_bop(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "BOP",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 0.0},
                {"timestamp": "01/03/2020", "data": 0.0},
                {"timestamp": "01/04/2020", "data": 0.0},
                {"timestamp": "01/05/2020", "data": 0.0},
            ],
        )

    def test_compute_cci(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "CCI",
                "lookback_period": 3,
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": 100.0},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_cmo(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "CMO",
                "lookback_period": 3,
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_dx(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "DX",
                "lookback_period": 3,
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_rsi(self):
        payload = {
            **self.payload,
            "inputs": {"indicator_name": "RSI", "lookback_period": 3},
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_bb(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "BB",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 0.75},
                {"timestamp": "01/03/2020", "data": 0.8061862178},
                {"timestamp": "01/04/2020", "data": 0.8354101966},
                {"timestamp": "01/05/2020", "data": 0.8535533906},
            ],
        )

    def test_compute_db(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "DB",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 1.0},
                {"timestamp": "01/03/2020", "data": 1.0},
                {"timestamp": "01/04/2020", "data": 1.0},
                {"timestamp": "01/05/2020", "data": 1.0},
            ],
        )

    def test_compute_kama(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "KAMA",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 10.0},
                {"timestamp": "01/02/2020", "data": 10.0041623309},
                {"timestamp": "01/03/2020", "data": 10.0124696677},
                {"timestamp": "01/04/2020", "data": 10.0249047575},
                {"timestamp": "01/05/2020", "data": 10.0414504193},
            ],
        )

    def test_compute_kc(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "KC",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 0.0},
                {"timestamp": "01/03/2020", "data": 0.0},
                {"timestamp": "01/04/2020", "data": 0.0},
                {"timestamp": "01/05/2020", "data": 0.0},
            ],
        )

    def test_compute_mi(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "MI",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 0.0},
                {"timestamp": "01/03/2020", "data": 0.0},
                {"timestamp": "01/04/2020", "data": 0.0},
                {"timestamp": "01/05/2020", "data": 0.0},
            ],
        )

    def test_compute_stoch_osci(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "STOCH_OSCI",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": None},
                {"timestamp": "01/02/2020", "data": None},
                {"timestamp": "01/03/2020", "data": None},
                {"timestamp": "01/04/2020", "data": None},
                {"timestamp": "01/05/2020", "data": None},
            ],
        )

    def test_compute_trix(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "TRIX",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": -0.180262237},
                {"timestamp": "01/02/2020", "data": 0.01953125},
                {"timestamp": "01/03/2020", "data": 0.0707869557},
                {"timestamp": "01/04/2020", "data": 0.1603775886},
                {"timestamp": "01/05/2020", "data": 0.2906374999},
            ],
        )

    def test_compute_tsi(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "TSI",
            },
            "outputs": {"DATA_BLOCK-1-1": DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "01/01/2020", "data": 0.0},
                {"timestamp": "01/02/2020", "data": 100.0},
                {"timestamp": "01/03/2020", "data": 100.0},
                {"timestamp": "01/04/2020", "data": 100.0},
                {"timestamp": "01/05/2020", "data": 100.0},
            ],
        )

    def test_compute_opening_range_high_one_day(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "OR",
                "lookback_period": "3",
                "lookback_field": "high",
            },
            "outputs": {"DATA_BLOCK-1-1": INTRADAY_DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-01T09:30:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:40:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:50:00.000Z", "data": None},
                {"timestamp": "2020-01-01T10:00:00.000Z", "data": 12.0},
                {"timestamp": "2020-01-01T10:10:00.000Z", "data": 12.0},
            ],
        )

    def test_compute_opening_range_mid_one_day(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "OR",
                "lookback_period": "3",
                "lookback_field": "mid",
            },
            "outputs": {"DATA_BLOCK-1-1": INTRADAY_DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-01T09:30:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:40:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:50:00.000Z", "data": None},
                {"timestamp": "2020-01-01T10:00:00.000Z", "data": 11.0},
                {"timestamp": "2020-01-01T10:10:00.000Z", "data": 11.0},
            ],
        )

    def test_compute_opening_range_low_one_day(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "OR",
                "lookback_period": "3",
                "lookback_field": "low",
            },
            "outputs": {"DATA_BLOCK-1-1": INTRADAY_DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-01T09:30:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:40:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:50:00.000Z", "data": None},
                {"timestamp": "2020-01-01T10:00:00.000Z", "data": 10.0},
                {"timestamp": "2020-01-01T10:10:00.000Z", "data": 10.0},
            ],
        )

    def test_compute_opening_range_high_two_days(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "OR",
                "lookback_period": "3",
                "lookback_field": "high",
            },
            "outputs": {"DATA_BLOCK-1-1": INTRADAY_TWO_DAYS_DATA_BLOCK},
        }

        response = event_ingestor(payload)

        self.assertEqual(
            response,
            [
                {"timestamp": "2020-01-01T09:30:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:40:00.000Z", "data": None},
                {"timestamp": "2020-01-01T09:50:00.000Z", "data": None},
                {"timestamp": "2020-01-01T10:00:00.000Z", "data": 12.0},
                {"timestamp": "2020-01-01T10:10:00.000Z", "data": 12.0},
                {"timestamp": "2020-01-02T09:30:00.000Z", "data": None},
                {"timestamp": "2020-01-02T09:40:00.000Z", "data": None},
                {"timestamp": "2020-01-02T09:50:00.000Z", "data": None},
                {"timestamp": "2020-01-02T10:00:00.000Z", "data": 15.0},
                {"timestamp": "2020-01-02T10:10:00.000Z", "data": 15.0},
            ],
        )

    def test_compute_opening_range_error_not_supported_field(self):
        payload = {
            **self.payload,
            "inputs": {
                "indicator_name": "OR",
                "lookback_period": "3",
                "lookback_field": "volume",
            },
            "outputs": {"DATA_BLOCK-1-1": INTRADAY_TWO_DAYS_DATA_BLOCK},
        }

        with self.assertRaises(AssertionError):
            event_ingestor(payload)
