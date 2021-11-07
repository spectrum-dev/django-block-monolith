import pandas as pd
from pydantic import BaseModel

from data_block.one.alpha_vantage import get_us_stock_data
from utils.utils import validate_payload

from .exceptions import (
    DataBlockOneInputPayloadInvalidException,
    DataBlockOneInvalidCandlestickException,
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

    def map_candlestick_to_freq_date(candlestick):
        case = lambda x: x == candlestick
        if case("1min"):
            return "T"
        elif case("5min"):
            return "5min"
        elif case("15min"):
            return "15min"
        elif case("30min"):
            return "30min"
        elif case("60min"):
            return "H"
        elif case("1day"):
            return "D"
        elif case("1week"):
            return "D"
        elif case("1month"):
            return "D"
        else:
            raise DataBlockOneInvalidCandlestickException

    input = validate_payload(
        InputPayload, input, DataBlockOneInputPayloadInvalidException
    )

    response_df = get_us_stock_data(input.equity_name, data_type=input.candlestick)

    if response_df is not None:
        date_range = pd.date_range(
            input.start_date,
            input.end_date,
            freq=map_candlestick_to_freq_date(input.candlestick),
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
