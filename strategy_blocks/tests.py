from django.test import TestCase, Client

from strategy_blocks.blocks.backtest.main import run

# Create your tests here.
class BacktestBlock(TestCase):
    def test_backtest(self):
        request_payload = {
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

        port_vals, trades = run(
            request_payload["input"],
            request_payload["output"]["DATA_BLOCK-1-1"],
            request_payload["output"]["SIGNAL_BLOCK-1-1"],
        )

        assert port_vals == [
            {"value": 10000.0, "timestamp": "01/01/2020"},
            {"value": 8995.150000000009, "timestamp": "01/02/2020"},
            {"value": 18085.15000000001, "timestamp": "01/03/2020"},
        ]
        assert trades == [
            {
                "date": "01/02/2020",
                "symbol": "close",
                "order": "BUY",
                "monetary_amount": 100000.0,
                "trade_id": "",
                "stop_loss": "",
                "take_profit": "",
                "shares": 9090,
                "cash_value": 100989.9,
            }
        ]
