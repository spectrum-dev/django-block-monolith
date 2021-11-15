from functools import reduce
from typing import List

import pandas as pd

from utils.utils import format_signal_block_response


def run(outputs: dict) -> List[dict]:
    """
    AND Block: Generate signals where two input SIGNAL_BLOCK data points agree

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

    # If all orders are the same, any merged column can be the actual final column
    df_merged["order"] = df_merged["order_x"]

    return format_signal_block_response(df_merged, "timestamp", ["order"])


def _create_orders_df(orders):
    df = pd.DataFrame.from_records(orders)
    return df
