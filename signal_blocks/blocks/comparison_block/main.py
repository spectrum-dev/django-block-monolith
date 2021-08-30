import pandas as pd
from signal_blocks.blocks.comparison_block.events.comparison_events import *


def run(input, output):
    """
    Takes in elements from the form input and two DATA or COMPUTATIONAL blocks and perform logical comparisons on
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    input_blocks: Time series data from 2 blocks (either can be computational or data)
    """
    input_block_1_name = input["input_block_1_name"]
    input_block_1_field = input["input_block_1_field"]
    input_block_2_name = input["input_block_2_name"]
    input_block_2_field = input["input_block_2_field"]

    input_block_1 = _format_request(output[input_block_1_name])
    input_block_1 = input_block_1[["timestamp"][input_block_1_field]]
    input_block_1 = input_block_1.rename(columns={input_block_1_field: "comparison_field_1"})

    input_block_2 = _format_request(output[input_block_2_name])
    input_block_2 = input_block_2[["timestamp"][input_block_2_field]]
    input_block_2 = input_block_2.rename(columns={input_block_2_field: "comparison_field_2"})

    df_merged = pd.merge(input_block_1, input_block_2, on=["timestamp"], how="outer")
    df_merged = df_merged.set_index("timestamp")
    df_merged.sort_index(inplace=True)

    _comparison_func = None
    case = lambda x: x == input["comparison_type"]

    if case("LESS_THAN"):
        _comparison_func = less_than
    elif case("LESS_THAN_EQUAL"):
        _comparison_func = less_than_equal
    elif case("MORE_THAN"):
        _comparison_func = more_than
    elif case("MORE_THAN_EQUAL"):
        _comparison_func = more_than_equal

    response_df = _comparison_func(
        df_merged,
        input["event_action"],
    )

    response = _format_response(response_df)
    return {"response": response}


def _format_request(request_json):
    """
    Helper method to format request
    """
    df = pd.DataFrame.from_records(request_json)
    return df


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
