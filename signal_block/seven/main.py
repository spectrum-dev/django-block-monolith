import pandas as pd
from pydantic import BaseModel

from signal_block.seven.events.comparison_events import *
from utils.utils import format_signal_block_response, validate_payload

from .exceptions import (
    SignalBlockSevenInputBlockOneMissingDataFieldException,
    SignalBlockSevenInputBlockTwoMissingDataFieldException,
    SignalBlockSevenInvalidComparisonTypeException,
    SignalBlockSevenInvalidInputPayloadException,
    SignalBlockSevenMissingInputBlockOneException,
    SignalBlockSevenMissingInputBlockTwoException,
    SignalBlockSevenMissingInputException,
)


class InputPayload(BaseModel):
    incoming_data_one: str
    incoming_data_two: str
    comparison_type: str
    event_action: str


def run(input, output):
    """
    Takes in elements from the form input and two DATA or COMPUTATIONAL blocks and perform logical comparisons on
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    input_blocks: Time series data from 2 blocks (either can be computational or data)
    """
    input = validate_payload(
        InputPayload, input, SignalBlockSevenInvalidInputPayloadException
    )
    # Data comes in as BlockIDInFlow, we have to parse the available outputs to get the right dataset name
    # Field name and block ID also comes in as 1 variable split by '-'
    # E.g. Flow BlockID 2 means COMPUTATIONAL_BLOCK-1-2
    input_block_1_id, input_block_1_field = input.incoming_data_one.split("-")
    input_block_2_id, input_block_2_field = input.incoming_data_two.split("-")

    # Extracts Block Name from Block ID in Flow
    try:
        input_block_1_name = [x for x in output.keys() if x.endswith(input_block_1_id)][
            0
        ]
    except IndexError:
        raise SignalBlockSevenMissingInputBlockOneException
    try:
        input_block_2_name = [x for x in output.keys() if x.endswith(input_block_2_id)][
            0
        ]
    except IndexError:
        raise SignalBlockSevenMissingInputBlockTwoException

    comparison_type = input.comparison_type
    event_action = input.event_action

    if not all(
        x
        for x in [
            input_block_1_name,
            input_block_1_field,
            input_block_2_name,
            input_block_2_field,
            comparison_type,
            event_action,
        ]
    ):
        raise SignalBlockSevenMissingInputException

    if any(
        x not in output[input_block_1_name][0].keys()
        for x in ["timestamp", input_block_1_field]
    ):
        raise SignalBlockSevenInputBlockOneMissingDataFieldException

    if any(
        x not in output[input_block_2_name][0].keys()
        for x in ["timestamp", input_block_2_field]
    ):
        raise SignalBlockSevenInputBlockTwoMissingDataFieldException

    input_block_1 = _format_request(output[input_block_1_name])
    input_block_1 = input_block_1[["timestamp", input_block_1_field]]
    input_block_1 = input_block_1.rename(
        columns={input_block_1_field: "comparison_field_1"}
    )

    input_block_2 = _format_request(output[input_block_2_name])
    input_block_2 = input_block_2[["timestamp", input_block_2_field]]
    input_block_2 = input_block_2.rename(
        columns={input_block_2_field: "comparison_field_2"}
    )

    df_merged = pd.merge(input_block_1, input_block_2, on=["timestamp"], how="outer")
    df_merged = df_merged.set_index("timestamp")
    df_merged.sort_index(inplace=True)

    _comparison_func = None
    case = lambda x: x == comparison_type

    if case("<"):
        _comparison_func = less_than
    elif case("<="):
        _comparison_func = less_than_equal
    elif case(">"):
        _comparison_func = more_than
    elif case(">="):
        _comparison_func = more_than_equal
    else:
        raise SignalBlockSevenInvalidComparisonTypeException

    response_df = _comparison_func(
        df_merged,
        event_action,
    )

    response = format_signal_block_response(response_df, "timestamp", ["order"])
    return {"response": response}


def _format_request(request_json):
    """
    Helper method to format request
    """
    df = pd.DataFrame.from_records(request_json)
    return df
