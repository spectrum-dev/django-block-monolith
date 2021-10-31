from signal_block.six.events.close_above_events import *
from utils.utils import format_request


def run(input, output):
    """
    Takes in elements from the form input and a single COMPUTATIONAL_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """
    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "DATA_BLOCK" or key_breakup[0] == "BULK_DATA_BLOCK":
            data_block = output[key]
            break

    data_block_df = format_request(data_block, "timestamp")

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

    response = _format_response(response_df)
    return {"response": response}


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
