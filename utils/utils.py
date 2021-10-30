import pandas as pd


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
