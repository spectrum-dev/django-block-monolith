from functools import reduce

import pandas as pd
from pydantic import BaseModel

from signal_block.one.events.main import handle_intersect
from utils.utils import format_signal_block_response, validate_payload

from .exceptions import SignalBlockOneInvalidInputException


class InputPayload(BaseModel):
    event_action: str


def run(input, computational_block):
    """
    Takes in elements from the form input and multiple computational_block
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """
    computational_block_df = _format_request(computational_block)

    response_df = handle_intersect(computational_block_df)
    input = validate_payload(InputPayload, input, SignalBlockOneInvalidInputException)
    response_df["order"] = input.event_action

    return format_signal_block_response(response_df, "timestamp", ["order"])


def _format_request(data):
    df_list = []
    for k, v in data.items():
        df = pd.DataFrame(v)
        df = df.rename(columns={"data": k})
        df_list.append(df)

    df = reduce(lambda x, y: pd.merge(x, y, on="timestamp"), df_list)
    df = df.set_index("timestamp")

    return df
