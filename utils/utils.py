import json
from typing import List

import pandas as pd

from .exceptions import InvalidRequestException, KeyDoesNotExistException


def format_request(request_json: dict, key: str) -> pd.DataFrame:
    """
    Takes in a JSON List Payload and converts it to a pandas DataFrame

    Attributes
    -----------
    request_json: List of Json Objects
    key: The main key to index DataFrame by
    """
    # Ensures request_json is no None and has a value
    if request_json == None or request_json == []:
        raise InvalidRequestException

    # Checks if the key exists in the request JSON
    all_keys = request_json[0].keys()
    if key not in all_keys:
        raise KeyDoesNotExistException

    # Converts the JSON into a DataFrame with the key being the index
    request_df = pd.DataFrame(request_json)
    request_df = request_df.sort_values(by=key)
    request_df = request_df.set_index(key)

    return request_df


def format_computational_block_response(
    response_df: pd.DataFrame, index_key: str, index_data: str
):
    """
    Formats response for COMPUTATIONAL_BLOCKS into a JSON Payload

    Attributes
    -----------
    response_df: Incoming DataFrame
    index_key: Key data is indexed
    index_data: Data key that needs to be retrieved
    """
    response_df.index.name = index_key
    response_df.name = index_data

    response_json = response_df.reset_index().to_json(
        orient="records", date_format="iso"
    )
    response_json = json.loads(response_json)

    return response_json


def format_signal_block_response(
    response_df: pd.DataFrame, index_key: str, filter_columns: List[str]
):
    """
    Formats response for SIGNAL_BLOCKS into a JSON Payload

    Attributes
    -----------
    response_df: Incoming DataFrame
    index_key: Key data is indexed
    filter_columns: List of keys to be filtered
    """
    response_df = response_df.reset_index(level=index_key)
    response_df.drop(
        response_df.columns.difference([index_key] + filter_columns), 1, inplace=True
    )
    response_df = response_df.dropna()

    response_json = response_df.to_dict(orient="records")
    return response_json


def get_data_from_id_and_field(id_field_string, output):
    """
    id_field_string: string of form '1-volume' for example, DATA-BLOCK with a volume column.
    output: dictionary of connecting output datasets
    Returns a dataframe with timestamp and data column
    """
    block_id, data_field = id_field_string.split("-")
    # try:
    block_name = [x for x in output.keys() if x.endswith(block_id)][0]
    # except KeyError:
    #     # TODO throw error here for non existing block ID in output dictionary
    #     pass
    data = pd.DataFrame.from_records(output[block_name])
    # if data_field not in data.columns:
    #     # TODO throw error for field not in dataframe
    #     pass
    data = data[["timestamp", data_field]]
    data = data.set_index("timestamp")
    data = data.rename(columns={data_field: "data"})
    return data


def get_block_data_from_dict(block_type, output):
    """
    block_type: string of form 'DATA_BLOCK' or 'SIGNAL_BLOCK' etc.
    output: dictionary of connecting output datasets
    Returns dictionary item that matches with block type required
    """
    data = None
    # TODO: validate that cannot be more than 1 of block type?
    for key in output.keys():
        key_breakup = key.split("-")
        if key_breakup[0] == block_type:
            data = output[key]
            break
    return data


def _convert_dict_to_df(data_dict):
    """
    Generates a Data Block DF

    Attributes
    ----------

    data_block: Incoming Data Block DF
    """
    data_block_df = pd.DataFrame(data_dict)

    assert "timestamp" in data_block_df.columns

    data_block_df.timestamp = pd.to_datetime(data_block_df.timestamp)
    data_block_df = data_block_df.sort_values(by="timestamp")
    data_block_df = data_block_df.set_index("timestamp")
    return data_block_df
