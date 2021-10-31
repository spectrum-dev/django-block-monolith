from functools import reduce

import pandas as pd

from signal_block.two.events.downward_saddle import main as downward_saddle
from signal_block.two.events.upward_saddle import main as upward_saddle
from utils.utils import format_signal_block_response


def run(input, output):
    """
    Takes in elements from the form input and a single DATA_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    output: Time series data from a block
    """

    incoming_data_field = input.get("incoming_data", "")
    output_df = _format_request(output, incoming_data_field)

    response_df = None
    case = lambda x: x == input["saddle_type"]
    if case("UPWARD"):
        response_df = upward_saddle(
            output_df,
            input["event_action"],
            consecutive_up=int(input["consecutive_up"]),
            consecutive_down=int(input["consecutive_down"]),
        )
    elif case("DOWNWARD"):
        response_df = downward_saddle(
            output_df,
            input["event_action"],
            consecutive_down=int(input["consecutive_down"]),
            consecutive_up=int(input["consecutive_up"]),
        )
    else:
        pass

    return format_signal_block_response(response_df, "timestamp", ["order"])


def _format_request(data, incoming_data_field):
    df_list = []
    for k, v in data.items():
        df = pd.DataFrame(v)
        df = df[["timestamp", incoming_data_field]]
        df = df.rename(columns={incoming_data_field: "data"})
        df_list.append(df)

    df = reduce(lambda x, y: pd.merge(x, y, on="timestamp"), df_list)
    df = df.set_index("timestamp")

    return df
