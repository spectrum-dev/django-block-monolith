from signal_blocks.blocks.event_block.events.main import handle_intersect, handle_not_implemented

def run(input, computational_block):
    """
        Takes in elements from the form input and multiple COMPUTATIONAL_BLOCKS
        to generates a series of events associated with that block

        Attributes
        ----------
        input: Form Inputs
        computational_block: Time series data from a computational block
    """
    
    computational_block_df = _format_request(computational_block)
    
    # Dictionary of supported events
    EVENT_MAP = {
        "INTERSECT": handle_intersect(computational_block_df),
        "NOT_IMPLEMENTED": handle_not_implemented(event_type)
    }
    
    # TODO: Should potentially raise an error here?
    response_df = EVENT_MAP.get(input["event_type"], "NOT_IMPLEMENTED")

    return _format_response(response_df)

def _format_request(data):
    df_list = []
    for k, v in data.items():
        df = pd.DataFrame(v)
        df = df.rename(columns={"data": k})
        df_list.append(df)
    
    df = reduce(lambda x, y: pd.merge(x, y, on = 'timestamp'), df_list)
    df = df.set_index("timestamp")

    return df

def _format_response(action, response_df):
    response_df["timestamp"] = response_df.index
    response_df["order"] = action
    response_df.drop(response_df.columns.difference(['timestamp', 'order']), 1, inplace=True)
    
    response_json = response_df.to_dict(orient="records")
    return response_json