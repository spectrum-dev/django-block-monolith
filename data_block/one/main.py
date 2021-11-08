import pandas as pd
from pydantic import BaseModel

from data_block.one.alpha_vantage import get_us_stock_data
from utils.utils import validate_payload

from .exceptions import (
    DataBlockOneInvalidCandlestickException,
    DataBlockOneInvalidInputPayloadException,
)


class InputPayload(BaseModel):
    equity_name: str
    candlestick: str
    start_date: str
    end_date: str


def run(input):
    """
    Runs a query to get the US stock data

    Attributes
    ----------
    input: The input payload
    """

    input = validate_payload(
        InputPayload, input, DataBlockOneInvalidInputPayloadException
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
        formatted_candlestick = "D"
    elif case("1month"):
        formatted_candlestick = "D"
    else:
        raise DataBlockOneInvalidCandlestickException

    response_df = get_us_stock_data(input.equity_name, data_type=input.candlestick)

    if response_df is not None:
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
    else:
        return {"response": []}
