import json

from django.test import TestCase

from strategy_blocks.blocks.simple_backtest.main import run

# Create your tests here.
class BacktestBlockValidation(TestCase):
    def test_backtest_zero_start_value_returns_error(self):
        payload = {
            "input": {
                "start_value": 0.00,
                "commission": 4.95,
                "impact": 0.00,
                "stop_loss": 0.00,
                "take_profit": 0.00,
                "trade_amount_value": 0.00,
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
                    }
                ],
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "BUY"}],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Start value must be greater than 0"]},
        )

    def test_backtest_empty_outputs_in_payload_returns_error(self):
        payload = {
            "input": {
                "start_value": 1000.00,
                "commission": 4.95,
                "impact": 0.00,
                "stop_loss": 0.00,
                "take_profit": 0.00,
                "trade_amount_value": 10.00,
            },
            "output": {},
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(), {"outputs_error": "You must have at least two output keys"}
        )

    def test_backtest_missing_data_block_in_outputs_returns_error(self):
        payload = {
            "input": {
                "start_value": 1000.00,
                "commission": 4.95,
                "impact": 0.00,
                "stop_loss": 0.00,
                "take_profit": 0.00,
                "trade_amount_value": 100.00,
            },
            "output": {
                "DATA_BLOCK_INVALID-1-1": [],
                "SIGNAL_BLOCK-1-1": [],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(
            response.json(),
            {"outputs_error": "You must have a DATA_BLOCK in the outputs payload"},
        )

    def test_backtest_missing_signal_block_in_outputs_returns_error(self):
        payload = {
            "input": {
                "start_value": 1000.00,
                "commission": 4.95,
                "impact": 0.00,
                "stop_loss": 0.00,
                "take_profit": 0.00,
                "trade_amount_value": 100.00,
            },
            "output": {
                "DATA_BLOCK-1-1": [],
                "SIGNAL_BLOCK_INVALID-1-1": [],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(
            response.json(),
            {"outputs_error": "You must have a SIGNAL_BLOCK in the outputs payload"},
        )

    def test_backtest_empty_output_block_data_returns_error(self):
        payload = {
            "input": {
                "start_value": 1000.00,
                "commission": 4.95,
                "impact": 0.00,
                "stop_loss": 0.00,
                "take_profit": 0.00,
                "trade_amount_value": 100.00,
            },
            "output": {
                "DATA_BLOCK-1-1": [],
                "SIGNAL_BLOCK-1-1": [],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(
            response.json(),
            {"outputs_error": "Data for outputs must have more than one entry"},
        )


class BacktestBlockRunning(TestCase):
    def test_backtest_block_buy_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 10090.0, "timestamp": "01/03/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "BUY",
                            "cash_allocated": 1000.0,
                            "shares": 90,
                            "amount_invested": 990.0,
                        }
                    ],
                }
            },
        )

    def test_backtest_block_sell_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                "SIGNAL_BLOCK-1-1": [{"timestamp": "01/02/2020", "order": "SELL"}],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 9910.0, "timestamp": "01/03/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "SELL",
                            "cash_allocated": 1000.0,
                            "shares": -90,
                            "amount_invested": -990.0,
                        }
                    ],
                }
            },
        )

    # TODO: There is a bug here (or is there?)
    def test_buy_sell_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "SELL"},
                ],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        # Bug -> It is due to price of the stock going up, hence it does not sell all shares. Need to distinguish between a "closing out" order and a SELL
        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 10090.0, "timestamp": "01/03/2020"},
                        {"value": 10180.0, "timestamp": "01/04/2020"},
                        {"value": 10180.0, "timestamp": "01/05/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "BUY",
                            "cash_allocated": 1000.0,
                            "shares": 90,
                            "amount_invested": 990.0,
                        },
                        {
                            "timestamp": "01/04/2020",
                            "order": "SELL_CLOSE",
                            "cash_allocated": 0.0,
                            "shares": -90,
                            "amount_invested": -1170.0,
                        },
                    ],
                }
            },
        )

    def test_sell_buy_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 9910.0, "timestamp": "01/03/2020"},
                        {"value": 9820.0, "timestamp": "01/04/2020"},
                        {"value": 9820.0, "timestamp": "01/05/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "SELL",
                            "cash_allocated": 1000.0,
                            "shares": -90,
                            "amount_invested": -990.0,
                        },
                        {
                            "timestamp": "01/04/2020",
                            "order": "BUY_CLOSE",
                            "cash_allocated": 0.0,
                            "shares": 90,
                            "amount_invested": 1170.0,
                        },
                    ],
                }
            },
        )

    def test_consecutive_sell_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/04/2020", "order": "SELL"},
                ],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 9910.0, "timestamp": "01/03/2020"},
                        {"value": 9820.0, "timestamp": "01/04/2020"},
                        {"value": 9654.0, "timestamp": "01/05/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "SELL",
                            "cash_allocated": 1000.0,
                            "shares": -90,
                            "amount_invested": -990.0,
                        },
                        {
                            "timestamp": "01/04/2020",
                            "order": "SELL",
                            "cash_allocated": 1000.0,
                            "shares": -76,
                            "amount_invested": -988.0,
                        },
                    ],
                }
            },
        )

    def test_consecutive_buy_ok(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 10090.0, "timestamp": "01/03/2020"},
                        {"value": 10180.0, "timestamp": "01/04/2020"},
                        {"value": 10346.0, "timestamp": "01/05/2020"},
                    ],
                    "trades": [
                        {
                            "timestamp": "01/02/2020",
                            "order": "BUY",
                            "cash_allocated": 1000.0,
                            "shares": 90,
                            "amount_invested": 990.0,
                        },
                        {
                            "timestamp": "01/04/2020",
                            "order": "BUY",
                            "cash_allocated": 1000.0,
                            "shares": 76,
                            "amount_invested": 988.0,
                        },
                    ],
                }
            },
        )

    def test_orders_df_empty(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [],
            },
        }

        response = self.client.post(
            "/STRATEGY_BLOCK/1/run",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(),
            {"outputs_error": "Data for outputs must have more than one entry"},
        )

    def test_orders_df_empty_core_function(self):
        payload = {
            "input": {
                "start_value": 10000.00,
                "commission": 0.00,
                "impact": 0.00,
                "stop_loss": 0.0,
                "take_profit": 0.0,
                "trade_amount_value": 1000.00,
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
                ],
                "SIGNAL_BLOCK-1-1": [],
            },
        }

        response = run(payload["input"], payload["output"])

        self.assertDictEqual(response, {"response": {"portVals": [], "trades": []}})
