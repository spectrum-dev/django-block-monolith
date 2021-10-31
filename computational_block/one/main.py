import json

from computational_block.one.momentum import *
from computational_block.one.mappings import INDICATORS


def run(input, output):
    """
    Takes in elements from the form input, and a DATA_BLOCK to create a technical analysis signal

    Attributes
    ----------
    input: Form inputs provided in metadata
    data_block: Data from a data_block stream
    """
    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == "DATA_BLOCK" or key_breakup[0] == "BULK_DATA_BLOCK":
            data_block = output[key]
            break

    data_block_df = _format_request(data_block)
    response = calculate_indicator(input, data_block_df)
    return _format_response(response)


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


def _format_request(request_json):
    """
    Helper method to format request
    """
    request_df = pd.DataFrame(request_json)
    request_df = request_df.sort_values(by="timestamp")
    request_df = request_df.set_index("timestamp")

    return request_df


def _format_response(response_df):
    """
    Helper method to format response
    """
    response_df.index.name = "timestamp"
    response_df.name = "data"
    response_json = response_df.reset_index().to_json(
        orient="records", date_format="iso"
    )
    response_json = json.loads(response_json)

    return response_json
