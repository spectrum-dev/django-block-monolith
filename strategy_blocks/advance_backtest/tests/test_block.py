import json

from django.test import TestCase
from blocks.event import event_ingestor


class BacktestBlockRunning(TestCase):
    maxDiff = None

    def test_backtest_block_simple_scenario(self):
        payload = {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 2,
            "inputs": {
                "start_value": 10000.00,
                "commission": 2.00,
                "stop_loss": 0.25,
                "take_profit": 0.50,
                "trade_amount_value": 1000.00,
            },
            "outputs": {
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
                    {"timestamp": "01/03/2020", "order": "SELL"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                ],
            },
        }

        response = event_ingestor(payload)
        # import pprint
        # print(pprint.pprint(response, width=1))
        self.assertDictEqual(
            response,
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020 00:00:00"},
                        {"value": 9998.0, "timestamp": "01/02/2020 00:00:00"},
                        {"value": 10086.0, "timestamp": "01/03/2020 00:00:00"},
                        {"value": 10084.0, "timestamp": "01/04/2020 00:00:00"},
                        {"value": 10160.0, "timestamp": "01/05/2020 00:00:00"},
                    ],
                    "trades": [
                        {
                            "amount_invested": 990.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 90,
                            "timestamp": "01/02/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1080.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 90,
                            "timestamp": "01/03/2020 00:00:00",
                        },
                        {
                            "amount_invested": 988.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 76,
                            "timestamp": "01/04/2020 00:00:00",
                        },
                    ],
                }
            },
        )

    def test_backtest_block_buy_hold_sell_all(self):
        payload = {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 2,
            "inputs": {
                "start_value": 10000.00,
                "commission": 2.00,
                "stop_loss": 0.25,
                "take_profit": 0.50,
                "trade_amount_value": 1000.00,
            },
            "outputs": {
                "DATA_BLOCK-1-1": [
                    {
                        "timestamp": "01/01/2020",
                        "close": "2.00",
                    },
                    {
                        "timestamp": "01/02/2020",
                        "close": "4.00",
                    },
                    {
                        "timestamp": "01/03/2020",
                        "close": "5.00",
                    },
                    {
                        "timestamp": "01/04/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/05/2020",
                        "close": "12.00",
                    },
                    {
                        "timestamp": "01/06/2020",
                        "close": "14.00",
                    },
                    {
                        "timestamp": "01/07/2020",
                        "close": "16.00",
                    },
                    {
                        "timestamp": "01/08/2020",
                        "close": "18.00",
                    },
                    {
                        "timestamp": "01/09/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/10/2020",
                        "close": "20.00",
                    },
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                    {"timestamp": "01/06/2020", "order": "BUY"},
                    {"timestamp": "01/10/2020", "order": "SELL"},
                ],
            },
        }

        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020 00:00:00"},
                        {"value": 9998.0, "timestamp": "01/02/2020 00:00:00"},
                        {"value": 10248.0, "timestamp": "01/03/2020 00:00:00"},
                        {"value": 11494.0, "timestamp": "01/04/2020 00:00:00"},
                        {"value": 11694.0, "timestamp": "01/05/2020 00:00:00"},
                        {"value": 11892.0, "timestamp": "01/06/2020 00:00:00"},
                        {"value": 12232.0, "timestamp": "01/07/2020 00:00:00"},
                        {"value": 12374.0, "timestamp": "01/08/2020 00:00:00"},
                        {"value": 12516.0, "timestamp": "01/09/2020 00:00:00"},
                        {"value": 12514.0, "timestamp": "01/10/2020 00:00:00"},
                    ],
                    "trades": [
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 250,
                            "timestamp": "01/02/2020 00:00:00",
                        },
                        {
                            "amount_invested": 2500.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 250,
                            "timestamp": "01/04/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 100,
                            "timestamp": "01/04/2020 00:00:00",
                        },
                        {
                            "amount_invested": 994.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 71,
                            "timestamp": "01/06/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1600.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 100,
                            "timestamp": "01/07/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1420.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 71,
                            "timestamp": "01/10/2020 00:00:00",
                        },
                    ],
                }
            },
        )

    def test_backtest_block_buy_hold_tp_sl(self):
        payload = {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 2,
            "inputs": {
                "start_value": 10000.00,
                "commission": 2.00,
                "stop_loss": 0.25,
                "take_profit": 0.50,
                "trade_amount_value": 1000.00,
            },
            "outputs": {
                "DATA_BLOCK-1-1": [
                    {
                        "timestamp": "01/01/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/02/2020",
                        "close": "8.00",
                    },
                    {
                        "timestamp": "01/03/2020",
                        "close": "5.00",
                    },
                    {
                        "timestamp": "01/04/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/05/2020",
                        "close": "12.00",
                    },
                    {
                        "timestamp": "01/06/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/07/2020",
                        "close": "16.00",
                    },
                    {
                        "timestamp": "01/08/2020",
                        "close": "18.00",
                    },
                    {
                        "timestamp": "01/09/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/10/2020",
                        "close": "20.00",
                    },
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/05/2020", "order": "BUY"},
                    {"timestamp": "01/08/2020", "order": "BUY"},
                ],
            },
        }

        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": {
                    "portVals": [
                        {"value": 9998.0, "timestamp": "01/01/2020 00:00:00"},
                        {"value": 9798.0, "timestamp": "01/02/2020 00:00:00"},
                        {"value": 9496.0, "timestamp": "01/03/2020 00:00:00"},
                        {"value": 9496.0, "timestamp": "01/04/2020 00:00:00"},
                        {"value": 9494.0, "timestamp": "01/05/2020 00:00:00"},
                        {"value": 10156.0, "timestamp": "01/06/2020 00:00:00"},
                        {"value": 10156.0, "timestamp": "01/07/2020 00:00:00"},
                        {"value": 10154.0, "timestamp": "01/08/2020 00:00:00"},
                        {"value": 10264.0, "timestamp": "01/09/2020 00:00:00"},
                        {"value": 10264.0, "timestamp": "01/10/2020 00:00:00"},
                    ],
                    "trades": [
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 100,
                            "timestamp": "01/01/2020 00:00:00",
                        },
                        {
                            "amount_invested": 500.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 100,
                            "timestamp": "01/03/2020 00:00:00",
                        },
                        {
                            "amount_invested": 996.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 83,
                            "timestamp": "01/05/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1660.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 83,
                            "timestamp": "01/06/2020 00:00:00",
                        },
                        {
                            "amount_invested": 990.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 55,
                            "timestamp": "01/08/2020 00:00:00",
                        },
                    ],
                }
            },
        )

    def test_backtest_block_mixed_buy_sell_no_tp_sl(self):
        payload = {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 2,
            "inputs": {
                "start_value": 10000.00,
                "commission": 2.00,
                "stop_loss": 999,
                "take_profit": 999,
                "trade_amount_value": 1000.00,
            },
            "outputs": {
                "DATA_BLOCK-1-1": [
                    {
                        "timestamp": "01/01/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/02/2020",
                        "close": "8.00",
                    },
                    {
                        "timestamp": "01/03/2020",
                        "close": "5.00",
                    },
                    {
                        "timestamp": "01/04/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/05/2020",
                        "close": "12.00",
                    },
                    {
                        "timestamp": "01/06/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/07/2020",
                        "close": "16.00",
                    },
                    {
                        "timestamp": "01/08/2020",
                        "close": "18.00",
                    },
                    {
                        "timestamp": "01/09/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/10/2020",
                        "close": "20.00",
                    },
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/01/2020", "order": "BUY"},
                    {"timestamp": "01/02/2020", "order": "BUY"},
                    {"timestamp": "01/03/2020", "order": "BUY"},
                    {"timestamp": "01/06/2020", "order": "SELL"},
                    {"timestamp": "01/08/2020", "order": "BUY"},
                    {"timestamp": "01/09/2020", "order": "BUY"},
                ],
            },
        }

        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": {
                    "portVals": [
                        {"value": 9998.0, "timestamp": "01/01/2020 00:00:00"},
                        {"value": 9796.0, "timestamp": "01/02/2020 00:00:00"},
                        {"value": 9119.0, "timestamp": "01/03/2020 00:00:00"},
                        {"value": 11244.0, "timestamp": "01/04/2020 00:00:00"},
                        {"value": 12094.0, "timestamp": "01/05/2020 00:00:00"},
                        {"value": 15492.0, "timestamp": "01/06/2020 00:00:00"},
                        {"value": 15492.0, "timestamp": "01/07/2020 00:00:00"},
                        {"value": 15490.0, "timestamp": "01/08/2020 00:00:00"},
                        {"value": 15598.0, "timestamp": "01/09/2020 00:00:00"},
                        {"value": 15598.0, "timestamp": "01/10/2020 00:00:00"},
                    ],
                    "trades": [
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 100,
                            "timestamp": "01/01/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 125,
                            "timestamp": "01/02/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 200,
                            "timestamp": "01/03/2020 00:00:00",
                        },
                        {
                            "amount_invested": 8500.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL_CLOSE",
                            "shares": 425,
                            "timestamp": "01/06/2020 00:00:00",
                        },
                        {
                            "amount_invested": 990.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 55,
                            "timestamp": "01/08/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY",
                            "shares": 50,
                            "timestamp": "01/09/2020 00:00:00",
                        },
                    ],
                }
            },
        )

    def test_backtest_block_short_sell(self):
        payload = {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 2,
            "inputs": {
                "start_value": 10000.00,
                "commission": 2.00,
                "stop_loss": 999,
                "take_profit": 999,
                "trade_amount_value": 1000.00,
            },
            "outputs": {
                "DATA_BLOCK-1-1": [
                    {
                        "timestamp": "01/01/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/02/2020",
                        "close": "8.00",
                    },
                    {
                        "timestamp": "01/03/2020",
                        "close": "5.00",
                    },
                    {
                        "timestamp": "01/04/2020",
                        "close": "10.00",
                    },
                    {
                        "timestamp": "01/05/2020",
                        "close": "12.00",
                    },
                    {
                        "timestamp": "01/06/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/07/2020",
                        "close": "16.00",
                    },
                    {
                        "timestamp": "01/08/2020",
                        "close": "18.00",
                    },
                    {
                        "timestamp": "01/09/2020",
                        "close": "20.00",
                    },
                    {
                        "timestamp": "01/10/2020",
                        "close": "20.00",
                    },
                ],
                "SIGNAL_BLOCK-1-1": [
                    {"timestamp": "01/01/2020", "order": "SELL"},
                    {"timestamp": "01/02/2020", "order": "SELL"},
                    {"timestamp": "01/04/2020", "order": "BUY"},
                    {"timestamp": "01/08/2020", "order": "SELL"},
                    {"timestamp": "01/09/2020", "order": "SELL"},
                ],
            },
        }

        response = event_ingestor(payload)
        self.assertDictEqual(
            response,
            {
                "response": {
                    "portVals": [
                        {"value": 9998.0, "timestamp": "01/01/2020 00:00:00"},
                        {"value": 10196.0, "timestamp": "01/02/2020 00:00:00"},
                        {"value": 10871.0, "timestamp": "01/03/2020 00:00:00"},
                        {"value": 9744.0, "timestamp": "01/04/2020 00:00:00"},
                        {"value": 9744.0, "timestamp": "01/05/2020 00:00:00"},
                        {"value": 9744.0, "timestamp": "01/06/2020 00:00:00"},
                        {"value": 9744.0, "timestamp": "01/07/2020 00:00:00"},
                        {"value": 9742.0, "timestamp": "01/08/2020 00:00:00"},
                        {"value": 9630.0, "timestamp": "01/09/2020 00:00:00"},
                        {"value": 9630.0, "timestamp": "01/10/2020 00:00:00"},
                    ],
                    "trades": [
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL",
                            "shares": 100,
                            "timestamp": "01/01/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL",
                            "shares": 125,
                            "timestamp": "01/02/2020 00:00:00",
                        },
                        {
                            "amount_invested": 2250.0,
                            "cash_allocated": 1000.0,
                            "order": "BUY_CLOSE",
                            "shares": 225,
                            "timestamp": "01/04/2020 00:00:00",
                        },
                        {
                            "amount_invested": 990.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL",
                            "shares": 55,
                            "timestamp": "01/08/2020 00:00:00",
                        },
                        {
                            "amount_invested": 1000.0,
                            "cash_allocated": 1000.0,
                            "order": "SELL",
                            "shares": 50,
                            "timestamp": "01/09/2020 00:00:00",
                        },
                    ],
                }
            },
        )