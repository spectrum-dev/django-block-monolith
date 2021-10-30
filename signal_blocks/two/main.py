import pandas as pd
from functools import reduce

from signal_blocks.two.events.upward_saddle import main as upward_saddle
from signal_blocks.two.events.downward_saddle import (
    main as downward_saddle,
)


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

    return _format_response(response_df)


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


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
