import json

from django.test import TestCase

from strategy_blocks.blocks.backtest.main import run

# Create your tests here.
class BacktestBlock(TestCase):
    def test_backtest_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 4.95,
                "impact": 0.01,
                "stop_loss": 0.1,
                "take_profit": 0.1,
                "trade_amount_value": 10.00,
                "trade_amount_unit": "PERCENTAGE",
            },
            "output": {
                "DATA_BLOCK-1-1": [
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
                ],
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}],
            },
        }
        
        response = self.client.post(
            "/STRATEGY_BLOCK/1/run", json.dumps(payload), content_type="application/json"
        )

        self.assertDictEqual(
            response.json(),
            {'response': {'portVals': [{'value': 10000.0, 'timestamp': '01/01/2020'}, {'value': 8995.150000000009, 'timestamp': '01/02/2020'}, {'value': 18085.15000000001, 'timestamp': '01/03/2020'}], 'trades': [{'date': '01/02/2020', 'symbol': 'close', 'order': 'BUY', 'monetary_amount': 100000.0, 'trade_id': '', 'stop_loss': '', 'take_profit': '', 'shares': 9090, 'cash_value': 100989.9}]}}
        )
