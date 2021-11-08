from functools import reduce

import pandas as pd
from pydantic import BaseModel

from signal_block.two.events.downward_saddle import main as downward_saddle
from signal_block.two.events.upward_saddle import main as upward_saddle
from utils.utils import format_signal_block_response, validate_payload

from .exceptions import (
    SignalBlockTwoInvalidInputPayloadException,
    SignalBlockTwoInvalidSaddleTypeException,
)


class InputPayload(BaseModel):
    incoming_data: str
    saddle_type: str
    event_action: str
    consecutive_up: int
    consecutive_down: int


def run(input, output):
    """
    Takes in elements from the form input and a single DATA_BLOCK
    to generates a series of events associated with that block
    Attributes
    ----------
    input: Form Inputs
    output: Time series data from a block
    """

    input = validate_payload(
        InputPayload, input, SignalBlockTwoInvalidInputPayloadException
    )
    output_df = _format_request(output, input.incoming_data)

    response_df = None
    case = lambda x: x == input.saddle_type
    if case("UPWARD"):
        response_df = upward_saddle(
            output_df,
            input.event_action,
            consecutive_up=input.consecutive_up,
            consecutive_down=input.consecutive_down,
        )
    elif case("DOWNWARD"):
        response_df = downward_saddle(
            output_df,
            input.event_action,
            consecutive_down=input.consecutive_down,
            consecutive_up=input.consecutive_up,
        )
    else:
        raise SignalBlockTwoInvalidSaddleTypeException

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
