import json
from typing import List, Optional, Type

import pandas as pd
from pydantic import BaseModel, ValidationError

from .exceptions import (
    BlockDataDoesNotExistException,
    BlockDoesNotExistException,
    FieldDoesNotExistException,
    InvalidRequestException,
    KeyDoesNotExistException,
)


def format_request(request_json: dict, key: str) -> pd.DataFrame:
    """Takes in a JSON List Payload and converts it to a pandas DataFrame

    Args:
        request_json (dict): List of JSON objects
        key (str): Main key to index DataFrame by

    Raises:
        InvalidRequestException: Named exception raised when request_json is empty
        KeyDoesNotExistException: Named exception raised when key is not found in JSON data

    Returns:
        pd.DataFrame: Returns a pandas DataFrame
    """
    # Ensures request_json is no None and has a value
    if request_json is None or request_json == []:
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
) -> dict:
    """Formats response for COMPUTATIONAL_BLOCKS into a JSON Payload

    Args:
        response_df (pd.DataFrame): Incoming pandas DataFrame
        index_key (str): String of column name that should be data's index
        index_data (str): Data key that needs to be retrieved

    Returns:
        dict: Returns a dictionary representation of dataframe
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
) -> dict:
    """Formats response for SIGNAL_BLOCKS into a JSON Payload

    Args:
        response_df (pd.DataFrame): Incoming pandas DataFrame
        index_key (str): String of column name that should be data's index
        filter_columns (List[str]): List of column names to subset data

    Returns:
        dict: Returns a dictionary representation of dataframe
    """

    response_df = response_df.reset_index(level=index_key)
    response_df.drop(
        response_df.columns.difference([index_key] + filter_columns), 1, inplace=True
    )
    response_df = response_df.dropna()

    response_json = response_df.to_dict(orient="records")
    return response_json


def retrieve_block_data(selectable_data: dict, incoming_data: dict) -> dict:
    """Pulls data from incoming payload when given a dictionary of block types

    Args:
        selectable_data (dict): Dictionary with keys used in return dictionary to specify required blocks. Contains block data that needs to be pulled in, e.g. {'data_block': ['DATA-BLOCK', 'BULK_DATA_BLOCK']}
        incoming_data (dict): Full output payload from flow

    Raises:
        BlockDataDoesNotExistException: Named exception raised when required block is not found in incoming_data payload

    Returns:
        dict: Returns a dictionary with keys as specified in selectable_data and items extracted from incoming_data
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
    """Helper function to convert string representation of block ID into dataframe representation

    Args:
        id_field_string (str): String representation of block ID and field mapping, e.g. '1-volume' for a DATA-BLOCK with a volume column
        output (dict): Dictionary of connecting output datasets

    Raises:
        BlockDoesNotExistException: Named exception raised when required block is not found in output dictionary
        FieldDoesNotExistException: Named exception raised when required field is not found in block data

    Returns:
        pd.DataFrame: Returns a pandas dataframe of data with timestamp as index and a 'data' column
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


def validate_payload(
    input_payload: Type[BaseModel],
    incoming_payload: dict,
    exception_raised: Exception,
    custom_exception: Optional[str] = None,
) -> Type[BaseModel]:
    """Helper function to validate Pydantic block input payload payload

    Args:
        input_payload (pydantic.BaseModel): Subclass of Pydantic BaseModel class with input variable types
        incoming_payload (dict): Input payload dictionary from flow
        exception_raised (Exception): Named exception class (subclass of python's Exception class) to override Pydantic's ValidationError
        custom_exception (Optional[str], optional): Custom exception text to be raised or defaults to Pydantic exception messages (None)

    Raises:
        exception_raised: Named Exception subclass of python's Exception class.

    Returns:
        BaseModel: Pydantic BaseModel object, input arguments can be called via class properties of the returned object
    """
    try:
        response = input_payload(**incoming_payload)
    except ValidationError as e:
        exception_text = custom_exception or str(e.json())
        raise exception_raised(exception_text)

    return response
