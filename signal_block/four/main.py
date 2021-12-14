from typing import List

from pydantic import BaseModel

from signal_block.four.events.crossover_above import main as crossover_above
from signal_block.four.events.crossover_below import main as crossover_below
from utils.types import EventActionEnum
from utils.utils import (
    format_signal_block_response,
    get_data_from_id_and_field,
    validate_payload,
)

from .exceptions import (
    SignalBlockFourInvalidEventTypeException,
    SignalBlockFourInvalidInputPayloadException,
)


class InputPayload(BaseModel):
    incoming_data: str
    event_type: str
    event_action: EventActionEnum
    event_value: float


def run(input: dict, output: dict) -> List[dict]:
    """
    Crossover Block: Generates signals based on whether one time series crosses over another
    time series

    Args:
        input (dict): Input payload from flow
        output (dict): Time series data from COMPUTATIONAL_BLOCK

    Raises:
        SignalBlockFourInvalidEventTypeException: Named exception raised when
            unsupported event type is used

    Returns:
        List[dict]: JSON representation of signal block data
    """
    input = validate_payload(
        InputPayload, input, SignalBlockFourInvalidInputPayloadException
    )

    computational_block_df = get_data_from_id_and_field(input.incoming_data, output)

    _crossover_func = None
    case = lambda x: x == input.event_type

    if case("ABOVE"):
        _crossover_func = crossover_above
    elif case("BELOW"):
        _crossover_func = crossover_below
    else:
        raise SignalBlockFourInvalidEventTypeException

    response_df = _crossover_func(
        computational_block_df,
        input.event_action.value,
        crossover_value=input.event_value,
    )
    return format_signal_block_response(response_df, "timestamp", ["order"])
