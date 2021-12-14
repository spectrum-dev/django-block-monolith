from typing import List

from pydantic import BaseModel

from signal_block.one.events.main import handle_intersect
from utils.types import EventActionEnum
from utils.utils import (
    format_signal_block_request,
    format_signal_block_response,
    validate_payload,
)

from .exceptions import SignalBlockOneInvalidInputPayloadException


class InputPayload(BaseModel):
    event_action: EventActionEnum


def run(input: dict, computational_block: dict) -> List[dict]:
    """
    Intersect Block: Generate signals where multiple COMPUTATIONAL_BLOCK time series
    data intersects

    Args:
        input (dict): Input payload from flow
        computational_block (dict): JSON representation of time series data from
            computational block

    Returns:
        List[dict]: JSON representation of signal block data
    """
    computational_block_df = format_signal_block_request(computational_block)

    response_df = handle_intersect(computational_block_df)
    input = validate_payload(
        InputPayload, input, SignalBlockOneInvalidInputPayloadException
    )
    response_df["order"] = input.event_action.value

    return format_signal_block_response(response_df, "timestamp", ["order"])
