import json
from typing import List

import pandas as pd

from .exceptions import (
    BlockDataDoesNotExistException,
    BlockDoesNotExistException,
    FieldDoesNotExistException,
    InvalidRequestException,
    KeyDoesNotExistException,
)


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


def retrieve_block_data(selectable_data, incoming_data):
    """
    Provided a dictionary of blocks it pulls data from the incoming payload

    Attributes
    ----------
    selectable_data: Dictionary containing block data that needs to be pulled in
    incoming_data: Full output payload
    """

    visited_keys = []

    response = {}
    for key, accepted_blocks in selectable_data.items():
        is_found = False
        for incoming_data_key, output_data in incoming_data.items():
            block_type = incoming_data_key.split("-")[0]
            if block_type in accepted_blocks and incoming_data_key not in visited_keys:
                visited_keys.append(incoming_data_key)
                response[key] = output_data
                is_found = True

        if not is_found:
            raise BlockDataDoesNotExistException

    return response


def get_data_from_id_and_field(id_field_string: str, output: dict) -> pd.DataFrame:
    """
    Provided a dictionary of blocks data and string denoting block ID and column-to-use, returns a dataframe with timestamp and data column.

    Attributes
    ----------
    id_field_string: string of form '1-volume' for example, DATA-BLOCK with a volume column.
    output: dictionary of connecting output datasets
    """
    block_id, data_field = id_field_string.split("-")
    block_names = [x for x in output.keys() if x.endswith(block_id)]
    # Has to have at least 1 block name that matches with block_id
    if not block_names:
        raise BlockDoesNotExistException
    block_name = block_names[0]
    data = pd.DataFrame.from_records(output[block_name])
    if data_field not in data.columns:
        raise FieldDoesNotExistException
    data = data[["timestamp", data_field]]
    data = data.set_index("timestamp")
    data = data.rename(columns={data_field: "data"})
    return data
<<<<<<< HEAD


def validate_payload(
    input_payload: BaseModel, incoming_payload: dict, exception_raised: Exception
<<<<<<< HEAD
) -> BaseModel:
=======
):
>>>>>>> 783eab5... make named exception more verbose and remove redundant exception
    try:
        response = input_payload(**incoming_payload)
    except ValidationError as e:
        raise exception_raised(str(e.json()))

    return response
=======
>>>>>>> bfb436f... remove and split up into different PRS
