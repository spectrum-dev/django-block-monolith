from functools import reduce
from typing import List

import pandas as pd


def run(outputs: dict) -> List[dict]:
    """
    OR Block: Generate signals where data point exist in either SIGNAL_BLOCK and
    does not contradict with each other (i.e. BUY and SELL at the same time)

    Args:
        outputs (dict): Time series data from COMPUTATIONAL_BLOCK

    Returns:
        List[dict]: JSON representation of signal block data
    """
    df_list = []
    for _, value in outputs.items():
        df = pd.DataFrame.from_records(value)
        if len(df) == 0:
            df = pd.DataFrame([], columns=["timestamp", "order"])
        df_list.append(df)

    # Checks for same date
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["timestamp"], how="outer"),
        df_list,
    )

    df_merged = df_merged.set_index("timestamp")
    df_merged.sort_index(inplace=True)

    # Checks if any orders is same as what is being checked
    df_merged = df_merged[df_merged.nunique(1).eq(1)]

    orders_response = _create_orders_json(df_merged)

    return orders_response


def _create_orders_json(orders_df):
    response = []
    for index, row in orders_df.iterrows():
        response.append(
            {
                "timestamp": index,
                "order": row.dropna()[0],
            }
        )

    return response
