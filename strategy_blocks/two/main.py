import math

import pandas as pd

from strategy_block.one.orders import Orders
from utils.utils import format_request, get_block_data_from_dict


def run(input, output):
    """
    Runs the backtest

    Attributes
    ----------
    input: Form Input Values
    output: Output Cache Values
    """
    data_block = get_block_data_from_dict("DATA_BLOCK", output)
    signal_block = get_block_data_from_dict("SIGNAL_BLOCK", output)
    portfolio_cash_value = float(input["start_value"])
    trade_commission = float(input["commission"])
    trade_amount = float(input["trade_amount_value"])

    if data_block is None or signal_block is None:
        return {"response": {"portVals": [], "trades": []}}

    # TODO: add validation for inputs

    price_df = format_request(data_block, "timestamp")
    signal_block_df = _generate_signal_block_df(signal_block)
    trades_df = _generate_trades_df(input, signal_block_df)

    held_units = 0
    final_orders = pd.DataFrame(
        {
            "timestamp": price_df.index[0],
            "portfolio_cash_value": [
                portfolio_cash_value,
            ],
            "held_units": [
                0,
            ],
            "order_type": [
                None,
            ],
            "order_units": [
                0,
            ],
            "order_unit_price": [
                None,
            ],
            "order_total_price": [
                None,
            ],
            "stop_loss": [
                None,
            ],
            "take_profit": [
                None,
            ],
            "monitor_to_close": [
                False,
            ],
        }
    )
    for i in range(len(price_df)):
        row = price_df.iloc[i]
        order_unit_price = float(row["close"])
        index = price_df.index[i]

        monitor_df = final_orders.copy()
        monitor_df = monitor_df.loc[final_orders["monitor_to_close"]]
        has_entry = False
        for j in range(len(monitor_df)):
            monitor_df_row = monitor_df.iloc[j]
            if (
                monitor_df_row["order_type"] == "BUY"
                and (
                    order_unit_price < monitor_df_row["stop_loss"]
                    or order_unit_price > monitor_df_row["take_profit"]
                )
            ) or (
                monitor_df_row["order_type"] == "SELL"
                and (
                    order_unit_price > monitor_df_row["stop_loss"]
                    or order_unit_price < monitor_df_row["take_profit"]
                )
            ):
                order_units = monitor_df_row["order_units"]
                order_total_price = order_unit_price * order_units
                if monitor_df_row["order_type"] == "BUY":
                    order_type = "SELL_CLOSE"
                    held_units -= order_units
                    portfolio_cash_value += order_total_price - trade_commission
                elif monitor_df_row["order_type"] == "SELL":
                    order_type = "BUY_CLOSE"
                    held_units += order_units
                    portfolio_cash_value -= order_total_price + trade_commission

                bool_arr = []
                counter = 0
                for k, v in final_orders.iterrows():
                    monitor_bool = v["monitor_to_close"]
                    if monitor_bool and counter == j:
                        monitor_bool = False
                    bool_arr.append(monitor_bool)
                final_orders["monitor_to_close"] = bool_arr

                # TODO: If 2 'closing' orders are present due to SL/TP trigger, these need to be combined into 1 order to save commission
                # Currently, it gets logged as 2 separate transactions (or N transactions closing N open trades) see test_backtest_block_short_sl_tp_buy_close
                final_orders = final_orders.append(
                    {
                        "timestamp": index,
                        "portfolio_cash_value": portfolio_cash_value,
                        "held_units": held_units,
                        "order_type": order_type,
                        "order_units": order_units,
                        "order_unit_price": order_unit_price,
                        "order_total_price": order_total_price,
                        "stop_loss": None,
                        "take_profit": None,
                        "monitor_to_close": False,
                    },
                    ignore_index=True,
                )
                has_entry = True

        if index in trades_df.index:
            trade = trades_df.loc[index]
            order_type = trade["order"]
            order_units = int(math.floor(trade["monetary_amount"] / order_unit_price))
            monitor_to_close = False
            if order_type == "BUY":
                stop_loss = order_unit_price * (1 - trade["stop_loss"])
                take_profit = order_unit_price * (1 + trade["take_profit"])
                held_units += order_units
                monitor_to_close = True
            elif order_type == "SELL":
                stop_loss = order_unit_price * (
                    1 + trade["stop_loss"]
                )  # If shorting, then stop loss is when price goes up
                take_profit = order_unit_price * (
                    1 - trade["take_profit"]
                )  # If shorting, then take profit is when price goes down
                held_units -= order_units
                monitor_to_close = True
            elif order_type in [
                "BUY_CLOSE",
                "SELL_CLOSE",
            ]:
                stop_loss = take_profit = None
                final_orders[
                    "monitor_to_close"
                ] = False  # All open trades should be closed at this point, no longer needed to be monitored
                order_units = abs(held_units)  # Sell or Buy all to close entire trade
                held_units = 0
            order_total_price = order_unit_price * order_units
            if "BUY" in order_type:
                portfolio_cash_value -= order_total_price + trade_commission
            elif "SELL" in order_type:
                portfolio_cash_value += order_total_price - trade_commission

            final_orders = final_orders.append(
                {
                    "timestamp": index,
                    "portfolio_cash_value": portfolio_cash_value,
                    "held_units": held_units,
                    "order_type": order_type,
                    "order_units": order_units,
                    "order_unit_price": order_unit_price,
                    "order_total_price": order_total_price,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "monitor_to_close": monitor_to_close,
                },
                ignore_index=True,
            )
            has_entry = True
        if not has_entry and i > 0:
            final_orders = final_orders.append(
                {
                    "timestamp": index,
                    "portfolio_cash_value": portfolio_cash_value,
                    "held_units": held_units,
                    "order_type": None,
                    "order_units": 0,
                    "order_unit_price": 0,
                    "order_total_price": 0,
                    "stop_loss": None,
                    "take_profit": None,
                    "monitor_to_close": False,
                },
                ignore_index=True,
            )
    port_val_df = price_df.copy(deep=True)
    port_val_df = port_val_df[["close"]]
    port_val_df = port_val_df.reset_index()
    port_val_df = pd.merge(port_val_df, final_orders, on="timestamp", how="left")
    port_val_df["value"] = port_val_df["held_units"].astype(float) * port_val_df[
        "close"
    ].astype(float) + port_val_df["portfolio_cash_value"].astype(float)
    print(port_val_df)
    port_val_df = port_val_df[["timestamp", "value"]]
    port_val_df["timestamp"] = port_val_df.timestamp.dt.strftime("%m/%d/%Y %H:%M:%S")
    port_val_df = port_val_df.drop_duplicates(
        keep="last",
        subset=[
            "timestamp",
        ],
    )
    port_vals = port_val_df.to_dict(orient="records")

    trades_df = final_orders.copy(deep=True)
    trades_df = trades_df[
        ["timestamp", "order_type", "order_units", "order_total_price"]
    ]
    trades_df = trades_df.loc[trades_df["order_type"].notnull()]
    trades_df = trades_df.rename(
        columns={
            "order_type": "order",
            "order_units": "shares",
            "order_total_price": "amount_invested",
        }
    )
    trades_df["cash_allocated"] = trade_amount
    trades_df["timestamp"] = trades_df.timestamp.dt.strftime("%m/%d/%Y %H:%M:%S")
    trades = trades_df.to_dict(orient="records")

    return {"response": {"portVals": port_vals, "trades": trades}}


def _generate_signal_block_df(signal_block):
    """
    Generates a dataframe for the signals

    Attributes
    ----------
    signal_block: Incoming Signal Block JSON
    """
    signal_block_df = pd.DataFrame(
        columns=["timestamp", "buy", "sell", "buy_close", "sell_close"],
    )
    signal_block_df = signal_block_df.set_index("timestamp")

    for i in range(0, len(signal_block)):
        # Returns boolean of whether should BUY or SELL
        buy = signal_block[i]["order"] == "BUY"
        sell = signal_block[i]["order"] == "SELL"
        not_purchased = True
        if i >= 1:
            if buy and signal_block_df.loc[i - 1]["sell"]:
                signal_block_df = signal_block_df.append(
                    {
                        "timestamp": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": False,
                        "buy_close": True,
                    },
                    ignore_index=True,
                )
                not_purchased = False
            elif sell and signal_block_df.loc[i - 1]["buy"]:
                signal_block_df = signal_block_df.append(
                    {
                        "timestamp": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": True,
                        "buy_close": False,
                    },
                    ignore_index=True,
                )
                not_purchased = False
        if not_purchased:
            signal_block_df = signal_block_df.append(
                {
                    "timestamp": signal_block[i]["timestamp"],
                    "buy": buy,
                    "sell": sell,
                    "sell_close": False,
                    "buy_close": False,
                },
                ignore_index=True,
            )

    if len(signal_block_df) > 0:
        signal_block_df = signal_block_df.set_index("timestamp")
    return signal_block_df


def _generate_trades_df(input, signal_block_df):
    """
    Generates the trades dataframe

    Attributes
    ----------
    input: Form Input
    signal_block_df: The DataFrame of signals generated earlier
    """
    orders = Orders()

    trade_amount = float(input["trade_amount_value"])
    stop_loss_pct = float(input["stop_loss"])
    take_profit_pct = float(input["take_profit"])

    for index, row in signal_block_df.iterrows():
        if row["buy"]:
            orders.buy(index, "close", trade_amount, "", stop_loss_pct, take_profit_pct)
        elif row["sell"]:
            orders.sell(
                index, "close", trade_amount, "", stop_loss_pct, take_profit_pct
            )
        elif row["buy_close"]:
            orders.buy_close(index, "close", "", "", "")
        elif row["sell_close"]:
            orders.sell_close(index, "close", "", "", "")

    trades_df = orders.trades_df
    if len(trades_df) > 0:
        trades_df.timestamp = pd.to_datetime(trades_df.timestamp)
        trades_df = trades_df.sort_values(by="timestamp")
        trades_df = trades_df.set_index("timestamp")

    return trades_df
