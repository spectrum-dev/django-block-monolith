from typing import List

from pydantic import BaseModel

from signal_block.six.events.close_above_events import *
from utils.types import EventActionEnum
from utils.utils import format_request, format_signal_block_response, validate_payload

from .exceptions import (
    SignalBlockSixInvalidEventTypeException,
    SignalBlockSixInvalidInputPayloadException,
    SignalBlockSixMissingDataFieldException,
)


class InputPayload(BaseModel):
    event_type: str
    event_action: EventActionEnum

    class Config:
        use_enum_values = True


def run(input: dict, output: dict) -> List[dict]:
    """
    Candle Close Block: Generate signals where DATA_BLOCK data points satisfy
    some characteristics

    Args:
        input (dict): Input payload from flow
        output (dict): Time series data from DATA_BLOCK

    Raises:
        SignalBlockSixInvalidEventTypeException: Named exception raised when
            unsupported event type is used

    Returns:
        List[dict]: JSON representation of signal block data
    """
    input = validate_payload(
        InputPayload, input, SignalBlockSixInvalidInputPayloadException
    )

    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "DATA_BLOCK" or key_breakup[0] == "BULK_DATA_BLOCK":
            data_block = output[key]
            break

    data_block_df = format_request(data_block, "timestamp")

    _candle_close_func = None
    case = lambda x: x == input.event_type

    if any([x not in data_block_df.columns for x in ["open", "high", "low", "close"]]):
        raise SignalBlockSixMissingDataFieldException

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
    else:
        raise SignalBlockSixInvalidEventTypeException

    response_df = _candle_close_func(
        data_block_df,
        input.event_action,
    )

    return format_signal_block_response(response_df, "timestamp", ["order"])
