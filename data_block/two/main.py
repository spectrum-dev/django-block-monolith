import pandas as pd
from pydantic import BaseModel

from data_block.two.alpha_vantage import get_crypto_data
from utils.utils import validate_payload

from .exceptions import (
    DataBlockTwoInvalidCandlestickException,
    DataBlockTwoInvalidInputPayloadException,
)


class InputPayload(BaseModel):
    crypto_name: str
    candlestick: str
    start_date: str
    end_date: str


def run(input: dict) -> dict:
    """
    Runs a query to get crypto data

    Args:
        input (dict): Input payload from flow

    Raises:
        DataBlockTwoInvalidCandlestickException: Named exception raised if
            candlestick type is not supported

    Returns:
        dict: Returns dictionary representation of dataframe
    """

    input = validate_payload(
        InputPayload, input, DataBlockTwoInvalidInputPayloadException
    )
    case = lambda x: x == input.candlestick
    if case("1min"):
        formatted_candlestick = "T"
    elif case("5min"):
        formatted_candlestick = "5min"
    elif case("15min"):
        formatted_candlestick = "15min"
    elif case("30min"):
        formatted_candlestick = "30min"
    elif case("60min"):
        formatted_candlestick = "H"
    elif case("1day"):
        formatted_candlestick = "D"
    elif case("1week"):
        formatted_candlestick = "W"
    elif case("1month"):
        formatted_candlestick = "M"
    else:
        raise DataBlockTwoInvalidCandlestickException

    response_df = get_crypto_data(input.crypto_name, input.candlestick)

    date_range = pd.date_range(
        input.start_date,
        input.end_date,
        freq=formatted_candlestick,
    )

    date_intersection = date_range.intersection(response_df.index)

    merged_df = pd.DataFrame(response_df, index=date_intersection)

    # Converts to JSON
    merged_df = merged_df.sort_index()
    merged_df["timestamp"] = merged_df.index.values.astype(str)
    response_dict = {"response": merged_df.to_dict(orient="records")}

    return response_dict
