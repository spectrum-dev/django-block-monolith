import pandas as pd

from signal_blocks.intersect_block.events.intersect import main


def handle_intersect(computational_block_df):
    """
    Handles the intersection between multiple indicators

    Attributes
    ----------
    df:
    """
    response = main(computational_block_df)

    return response
