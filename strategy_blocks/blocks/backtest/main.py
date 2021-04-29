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
    port_vals, trades_df = run_marketsim(trades_df, data_block_df, float(input["start_value"]), float(input["commission"]), float(input["impact"]))

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
    signal_block_df = pd.DataFrame(columns=['datetime', 'buy', 'sell'])

    for record in signal_block:        
        signal_block_df = signal_block_df.append({
            'datetime': record['timestamp'],
            'buy': record["order"] == 'BUY',
            'sell': record["order"] == 'SELL'
        }, ignore_index=True)

    signal_block_df = signal_block_df.set_index('datetime')

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

    #  TODO: Do we want a dropdown for the trade_amount_unit, and if so need to uncomment this logic
    # if (input["trade_amount_unit"] == "PERCENTAGE"):
    #     trade_amount = input["start_value"] * input["trade_amount_value"]
    # elif (input["trade_amount_unit"] == "NOMINAL"):
    #     trade_amount = input["trade_amount_value"]
    # else:
    #     raise ValueError(f"The unit {input['trade_amount_unit']} is not valid")

    trade_amount = float(input["start_value"]) * float(input["trade_amount_value"])

    for index, row in signal_block_df.iterrows():
        if row["buy"]:
            orders.buy(index, "close", trade_amount, "", "", "")
        elif row["sell"]:
            orders.sell(index, 'close', trade_amount, '', '', '')
        else:
            raise Exception("Both the BUY and SELL are empty")
        
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
    port_vals_df['timestamp'] = port_vals_df.index
    
    port_vals = port_vals_df.to_dict(orient='records')

    return port_vals

def _generate_trades_df_response(trades_df):
    """
        Generates JSON response from trades

        Attributes
        ----------
        trades_df: DataFrame of Trades
    """
    trades = trades_df.to_dict(orient='records')

    return trades