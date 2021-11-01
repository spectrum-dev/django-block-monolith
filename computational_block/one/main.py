from utils.utils import (
    format_computational_block_response,
    format_request,
    retrieve_block_data,
)

from .mappings import INDICATORS

from .momentum import *  # isort:skip


def run(input, output):
    """
    Takes in elements from the form input, and a DATA_BLOCK to create a technical analysis signal

    Attributes
    ----------
    input: Form inputs provided in metadata
    data_block: Data from a data_block stream
    """
    selectable_data = {"data_block": ["DATA_BLOCK", "BULK_DATA_BLOCK"]}

    block_data = retrieve_block_data(selectable_data, output)

    data_block_df = format_request(block_data["data_block"], "timestamp")
    response = calculate_indicator(input, data_block_df)
    return format_computational_block_response(response, "timestamp", "data")


def calculate_indicator(
    input,
    data_block_df,
):
    """
    Provided the form input and data that needs to be processed,
    this will form a stringified version of the python function
    and execute the function

    Attributes
    ----------
    input: Form Inputs
    data_block_df: Incoming Data from Flow in Pandas Form
    """
    # Retrieves function name of indicator being calculated
    function_name = INDICATORS[input["indicator_name"]]["functionName"]

    # Removes key from payload passed into run function
    input.pop("indicator_name", None)

    # Assembles a python function in string form to be executed
    i = 0
    parameters = "(data_block=data_block_df, "
    for k, v in input.items():
        if i == len(input.keys()) - 1:
            parameters += f"{k}='{v}'"
        else:
            parameters += f"{k}='{v}', "

        i += 1
    parameters += ")"

    # Executes string representation of function
    response = eval(f"{function_name}{parameters}")

    return response
