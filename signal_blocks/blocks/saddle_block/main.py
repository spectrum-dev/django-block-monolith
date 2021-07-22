import pandas as pd
from functools import reduce

from signal_blocks.blocks.saddle_block.events.upward_saddle import main as upward_saddle
from signal_blocks.blocks.saddle_block.events.downward_saddle import (
    main as downward_saddle,
)


def run(input, computational_block):
    """
    Takes in elements from the form input and a single DATA_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """
    computational_block_df = _format_request(computational_block)

    response_df = None
    case = lambda x: x == input["saddle_type"]
    if case("UPWARD"):
        response_df = upward_saddle(
            computational_block_df,
            input["event_action"],
            consecutive_up=int(input["consecutive_up"]),
            consecutive_down=int(input["consecutive_down"]),
        )
    elif case("DOWNWARD"):
        response_df = downward_saddle(
            computational_block_df,
            input["event_action"],
            consecutive_down=input["consecutive_down"],
            consecutive_up=input["consecutive_up"],
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
