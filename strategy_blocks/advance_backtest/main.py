import pandas as pd

from utils.utils import get_block_data_from_dict, _convert_dict_to_df
from strategy_blocks.simple_backtest.orders import Orders
import math


def run(input, output):
    """
    Runs the backtest

    Attributes
    ----------
    input: Form Input Values
    output: Output Cache Values
    """
    data_block = get_block_data_from_dict(["DATA_BLOCK", "BULK_DATA_BLOCK"], output)
    signal_block = get_block_data_from_dict("SIGNAL_BLOCK", output)
    portfolio_cash_value = float(input["start_value"])
    trade_commission = float(input["commission"])
    trade_amount = float(input["trade_amount_value"])

    if len(signal_block) <= 0 or len(data_block) <= 0:
        return {"response": {"portVals": [], "trades": []}}

    price_df = _convert_dict_to_df(data_block)
    signal_block_df = _generate_signal_block_df(signal_block)
    trades_df = _generate_trades_df(input, signal_block_df)

    held_units = 0
    final_orders = pd.DataFrame(
        {
            "timestamp": price_df.index[0],
            "portfolio_cash_value": [
                10000,
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
        }
    )

    for i in range(len(price_df)):
        row = price_df.iloc[i]
        order_unit_price = float(row["close"])
        index = price_df.index[i]
        monitor_df = final_orders.loc[final_orders["monitor_to_close"]]
        has_entry = False
        for j in range(len(monitor_df)):
            monitor_df_row = monitor_df.iloc[j]
            if (
                order_unit_price < monitor_df_row["stop_loss"]
                or order_unit_price > monitor_df_row["take_profit"]
            ):
                order_units = monitor_df_row["order_units"]
                order_total_price = order_unit_price * order_units
                # order_type = "SELL_CLOSE" if monitor_df_row["order_type"] == "BUY" else "BUY_CLOSE"
                if monitor_df_row["order_type"] == "BUY":
                    order_type = "SELL_CLOSE"
                    held_units -= order_units
                    portfolio_cash_value += order_total_price - trade_commission
                elif monitor_df_row["order_type"] == "SELL":
                    order_type = "BUY_CLOSE"
                    held_units += order_units
                    portfolio_cash_value -= order_total_price - trade_commission
                monitor_df.loc[j, "monitor_to_close"] = False

                final_orders.append(
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
            trade = trades_df.loc[trades_df.timestamp == index]
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
                order_units = held_units  # Sell or Buy all to close entire trade
                held_units = 0
            order_total_price = order_unit_price * order_units
            if "BUY" in order_type:
                portfolio_cash_value -= order_total_price - trade_commission
            elif "SELL" in order_type:
                portfolio_cash_value += order_total_price - trade_commission

            final_orders.append(
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
    if not has_entry:
        final_orders.append(
            {
                "timestamp": index,
                "portfolio_cash_value": portfolio_cash_value,
                "held_units": held_units,
                "order_type": "NONE",
                "order_units": 0,
                "order_unit_price": 0,
                "order_total_price": 0,
                "stop_loss": None,
                "take_profit": None,
                "monitor_to_close": False,
            },
            ignore_index=True,
        )
    # final_orders.append([portfolio_cash_value, held_units, order_type, units, price, stop_loss, take_profit, status])
    # TODO: Check signal
    # TODO: Check performance hit SL/TP
    # Do we exit based on total portfolio or last trade or specific trade?
    # TODO: append to trades df
    # Calculate portfolio value

    # TODO: Implement the marketsim
    # port_vals, trades_df = run_marketsim(
    #     trades_df,
    #     data_block_df,
    #     float(input["start_value"]),
    #     float(input["commission"]),
    # )

    port_val_df = price_df.copy(deep=True)
    port_val_df = port_val_df[["close"]]
    port_val_df["timestamp"] = port_val_df.index
    port_val_df = pd.merge(port_val_df, final_orders, on="timestamp", how="left")
    port_val_df["value"] = port_val_df["held_units"] * port_val_df["close"]
    port_val_df = port_val_df[["timestamp", "value"]]
    port_vals = port_val_df.to_dict(orient="records")
    # port_val_df["securities_value"] = port_val_df["held_units"] * 1
    # Generates Responses
    # port_vals = _generate_port_vals_response(port_vals)
    trades = _generate_trades_df_response(trades_df)

    trades_df = final_orders.copy(deep=True)
    trades_df = trades_df[
        ["timestamp", "order_type", "order_units", "order_total_price"]
    ]
    trades_df = trades_df.rename(
        {
            "order_type": "order",
            "order_units": "shares",
            "order_total_price": "amount_invested",
        }
    )
    trades_df["cash_allocated"] = trade_amount
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
            if buy and signal_block[i - 1]["order"] == "SELL":
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
            elif sell and signal_block[i - 1]["order"] == "BUY":
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
    stop_loss_pct = float(input["trade_stop_loss"])
    take_profit_pct = float(input["trade_take_profit"])

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

    return orders.trades_df


def _generate_port_vals_response(port_vals):
    """
    Generates JSON response from port_vals

    Attributes
    ----------
    port_vals: List of Portfolio Values
    """
    port_vals_df = port_vals.to_frame()
    port_vals_df = port_vals_df.rename(columns={0: "value"})
    port_vals_df["timestamp"] = port_vals_df.index

    port_vals = port_vals_df.to_dict(orient="records")

    return port_vals


def _generate_trades_df_response(trades_df):
    """
    Generates JSON response from trades

    Attributes
    ----------
    trades_df: DataFrame of Trades
    """
    trades_df = trades_df.drop(
        columns=["symbol", "trade_id", "stop_loss", "take_profit"]
    )

    trades_df = trades_df.rename(
        columns={
            "cash_value": "amount_invested",
            "monetary_amount": "cash_allocated",
        }
    )

    trades_df = trades_df.round(2)
    trades = trades_df.to_dict(orient="records")

    return trades
