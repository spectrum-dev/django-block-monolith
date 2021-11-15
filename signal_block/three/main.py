from functools import reduce
from typing import List

import pandas as pd


def run(outputs: dict) -> List[dict]:
    """
    Generate signals where two input SIGNAL_BLOCK data points agree

    Args:
        outputs (dict): Dictionary of SIGNAL_BLOCK to be used

    Returns:
        List[dict]: Returns a JSON representation of signal block data
    """
    df_list = []
    for _, value in outputs.items():
        df = _create_orders_df(value)
        if len(df) == 0:
            df = pd.DataFrame([], columns=["timestamp", "order"])
        df_list.append(df)

    # Checks for same date
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["timestamp"], how="outer"),
        df_list,
    )
    df_merged = df_merged.dropna()

    df_merged = df_merged.set_index("timestamp")

    # Checks if all orders are same
    df_merged = df_merged[df_merged.nunique(1).eq(1)]

    orders_response = _create_orders_json(df_merged)

    return orders_response


def _create_orders_df(orders):
    df = pd.DataFrame.from_records(orders)
    return df


def _create_orders_json(orders_df):
    response = []
    for index, row in orders_df.iterrows():
        response.append(
            {
                "timestamp": index,
                "order": row[0],
            }
        )

    return response
