import logging
import pandas as pd

from signal_blocks.blocks.event_block.events.intersect import main

def handle_intersect(computational_block_df):
    """
        Handles the intersection between multiple indicators

        Attributes
        ----------
        df: 
    """
    response = main(computational_block_df)

    return response

def handle_not_implemented(event_type):
    """
        Handles case where event type has not been implemented

        Attributes
        ----------
        event_type: ENUM representing event type
    """
    logging.error(f"The event type {event_type} has not been implemented")
    return None