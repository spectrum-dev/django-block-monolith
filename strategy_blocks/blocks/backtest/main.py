import pandas as pd

from strategy_blocks.blocks.backtest.orders import Orders
from strategy_blocks.blocks.backtest.marketsim import run as run_marketsim


def run(input, data_block, signal_block):
    """
    Runs the backtest

    Attributes
    ----------
    input: Form Input Values
    data_block: Data Block from output
    signal_block: Signal Block from output
    """
    data_block_df = _generate_data_block_df(data_block)
    signal_block_df = _generate_signal_block_df(signal_block)
    trades_df = _generate_trades_df(input, signal_block_df)

    # TODO: Implement the marketsim
    port_vals, trades_df = run_marketsim(
        trades_df,
        data_block_df,
        float(input["start_value"]),
        float(input["commission"]),
        float(input["impact"]),
    )

    # Generates Responses
    port_vals = _generate_port_vals_response(port_vals)
    trades = _generate_trades_df_response(trades_df)

    return port_vals, trades


def _generate_data_block_df(data_block):
    """
    Generates a Data Block DF

    Attributes
    ----------

    data_block: Incoming Data Block DF
    """
    data_block_df = pd.DataFrame(data_block)
    data_block_df = data_block_df.sort_values(by="timestamp")
    data_block_df = data_block_df.set_index("timestamp")

    return data_block_df


def _generate_signal_block_df(signal_block):
    """
    Generates a dataframe for the signals

    Attributes
    ----------
    signal_block: Incoming Signal Block JSON
    """
    signal_block_df = pd.DataFrame(
        columns=["datetime", "buy", "sell", "buy_close", "sell_close"]
    )

    for i in range(0, len(signal_block)):
        buy = signal_block[i]["order"] == "BUY"
        sell = signal_block[i]["order"] == "SELL"

        if i >= 1:
            if buy and signal_block[i - 1]["order"] == "SELL":
                signal_block_df = signal_block_df.append(
                    {
                        "datetime": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": False,
                        "buy_close": True,
                    },
                    ignore_index=True,
                )
            elif sell and signal_block[i - 1]["order"] == "BUY":
                signal_block_df = signal_block_df.append(
                    {
                        "datetime": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": True,
                        "buy_close": False,
                    },
                    ignore_index=True,
                )
        else:
            signal_block_df = signal_block_df.append(
                {
                    "datetime": signal_block[i]["timestamp"],
                    "buy": buy,
                    "sell": sell,
                    "sell_close": False,
                    "buy_close": False,
                },
                ignore_index=True,
            )

    signal_block_df = signal_block_df.set_index("datetime")

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

    for index, row in signal_block_df.iterrows():
        if row["buy"]:
            orders.buy(index, "close", trade_amount, "", "", "")
        elif row["sell"]:
            orders.sell(index, "close", trade_amount, "", "", "")
        elif row["buy_close"]:
            orders.buy_close(index, "close", "", "", "")
        elif row["sell_close"]:
            orders.sell_close(index, "close", "", "", "")
        else:
            raise Exception("The BUY, SELL, BUY_CLOSE and SELL_CLOSE options are empty")

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
    trades = trades_df.to_dict(orient="records")

    return trades
