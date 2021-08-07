import pandas as pd
from functools import reduce

from signal_blocks.blocks.crossover_block.events.crossover_above import (
    main as crossover_above,
)
from signal_blocks.blocks.crossover_block.events.crossover_below import (
    main as crossover_below,
)


def run(input, computational_block):
    """
    Takes in elements from the form input and a single COMPUTATIONAL_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """
    computational_block_df = _format_request(computational_block)

    response_df = None
    _crossover_func = None
    case = lambda x: x == input["event_type"]

    if case("ABOVE"):
        _crossover_func = crossover_above
    elif case("BELOW"):
        _crossover_func = crossover_below

    if _crossover_func is not None:
        response_df = _crossover_func(
            computational_block_df,
            input["event_action"],
            crossover_value=float(input["event_value"]),
        )
    else:
        pass

    return _format_response(response_df)


def _format_request(data):
    df_list = []
    for k, v in data.items():
        df = pd.DataFrame(v)
        df_list.append(df)

    df = reduce(lambda x, y: pd.merge(x, y, on="timestamp"), df_list)
    df = df.set_index("timestamp")

    return df


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
