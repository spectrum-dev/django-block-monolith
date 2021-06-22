from django.test import TestCase

from computational_blocks.blocks.technical_analysis.main import run
from computational_blocks.data.technical_analysis import DATA_BLOCK

class GetIndicator(TestCase):
    def test_ok(self):
        response = self.client.get(f'/COMPUTATIONAL_BLOCK/1/indicator')

        self.assertEqual(
            response.json(),
            {'response': ['MA', 'EMA', 'MACD', 'ADX', 'ADXR', 'APO', 'AROONOSC', 'BOP', 'CCI', 'CMO', 'DX', 'RSI']}
        )
class GetIndicatorField(TestCase):
    def test_ok(self):
        indicator_name = 'MA'
        response = self.client.get(f'/COMPUTATIONAL_BLOCK/1/indicatorField?indicatorName={indicator_name}')

        self.assertEqual(
            response.json(),
            {'response': [{'fieldName': 'Lookback Period', 'fieldType': 'input', 'fieldVariableName': 'lookback_period'}, {'fieldName': 'Lookback Unit', 'fieldType': 'dropdown', 'fieldVariableName': 'lookback_unit', 'fieldData': {'options': ['DATA_POINT']}}]}
        )
    
    def test_error_not_found(self):
        indicator_name = 'INDICATOR_DNE'
        response = self.client.get(f'/COMPUTATIONAL_BLOCK/1/indicatorField?indicatorName={indicator_name}')

        self.assertEqual(
            response.json(),
            {'error': 'The indicator INDICATOR_DNE was not found'}
        )

class PostRun(TestCase):
    def test_compute_ma(self):
        input = {
            "short_name": "MA",
            "indicator_name": "MA",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_ema(self):
        input = {
            "short_name": "EMA",
            "indicator_name": "EMA",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_macd(self):
        input = {
            "short_name": "MACD",
            "indicator_name": "MACD",
            "lookback_period_one": "2",
            "lookback_period_two": "3",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_adx(self):
        input = {
            "short_name": "ADX",
            "indicator_name": "ADX",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_adxr(self):
        input = {
            "short_name": "ADXR",
            "indicator_name": "ADXR",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_apo(self):
        input = {
            "short_name": "APO",
            "indicator_name": "APO",
            "fast_period": "2",
            "slow_period": "4",
            "ma_type": "0",
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_aroon_oscillator(self):
        input = {
            "short_name": "AROONOSC",
            "indicator_name": "AROONOSC",
            "lookback_period": 3,
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_bop(self):
        input = {
            "short_name": "BOP",
            "indicator_name": "BOP",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_cci(self):
        input = {
            "short_name": "CCI",
            "indicator_name": "CCI",
            "lookback_period": 3,
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_cmo(self):
        input = {
            "short_name": "CMO",
            "indicator_name": "CMO",
            "lookback_period": 3,
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_dx(self):
        input = {
            "short_name": "DX",
            "indicator_name": "DX",
            "lookback_period": 3,
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5

    def test_compute_rsi(self):
        input = {
            "short_name": "RSI",
            "indicator_name": "RSI",
            "lookback_period": 3,
            "lookback_unit": "DATA_POINT",
        }
        response = run(input, DATA_BLOCK)
        assert len(response) == 5