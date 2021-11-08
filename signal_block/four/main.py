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


def run(input, output):
    """
    Takes in elements from the form input and a single COMPUTATIONAL_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
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
        input.event_action,
        crossover_value=input.event_value,
    )
    return format_signal_block_response(response_df, "timestamp", ["order"])
