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
