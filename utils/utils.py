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
