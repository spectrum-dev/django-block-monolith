import pandas as pd

from functools import reduce

def run(input, outputs):
    event_action = input["event_action"]

    df_list = []
    for _, value in outputs.items():
        df = _create_orders_df(value)
        df_list.append(df)
    
    # Checks for same date
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['timestamp'], how='outer'), df_list)
    df_merged = df_merged.dropna()

    df_merged = df_merged.set_index('timestamp')

    # Checks if any orders is same as what is being checked
    df_merged = df_merged[df_merged.eq(event_action).any(1)]

    orders_response = _create_orders_json(df_merged, event_action)

    return orders_response

def _create_orders_df(orders):
    df = pd.DataFrame.from_records(orders)
    return df

def _create_orders_json(orders_df, event_action):
    response = []
    for index, row in orders_df.iterrows():
        response.append(
            {
                'timestamp': index,
                'order': event_action,
            }
        )
    
    return response
