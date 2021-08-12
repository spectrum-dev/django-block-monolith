import pandas as pd
from functools import reduce
import json

from signal_blocks.blocks.candle_close_block.events.close_above_open import (
    main as close_above_open,
)
from signal_blocks.blocks.candle_close_block.events.close_below_open import (
    main as close_below_open,
)
from signal_blocks.blocks.candle_close_block.events.close_eq_high import (
    main as close_eq_high,
)
from signal_blocks.blocks.candle_close_block.events.close_below_high import (
    main as close_below_high,
)
from signal_blocks.blocks.candle_close_block.events.close_above_low import (
    main as close_above_low,
)
from signal_blocks.blocks.candle_close_block.events.close_eq_low import (
    main as close_eq_low,
)


def run(input, data_block):
    """
    Takes in elements from the form input and a single COMPUTATIONAL_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """
    data_block_df = _format_request(data_block)

    _candle_close_func = None
    case = lambda x: x == input["event_type"]

    if case("CLOSE_ABOVE_OPEN"):
        _candle_close_func = close_above_open
    elif case("CLOSE_BELOW_OPEN"):
        _candle_close_func = close_below_open
    elif case("CLOSE_EQ_HIGH"):
        _candle_close_func = close_eq_high
    elif case("CLOSE_BELOW_HIGH"):
        _candle_close_func = close_below_high
    elif case("CLOSE_ABOVE_LOW"):
        _candle_close_func = close_above_low
    elif case("CLOSE_EQ_LOW"):
        _candle_close_func = close_eq_low

    response_df = _candle_close_func(
        data_block_df,
        input["event_action"],
    )
    return _format_response(response_df)


def _format_request(request_json):
    """
    Helper method to format request
    """
    request_df = pd.DataFrame(request_json)
    print(request_df)
    request_df = request_df.sort_values(by="timestamp")
    request_df = request_df.set_index("timestamp")

    return request_df


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
