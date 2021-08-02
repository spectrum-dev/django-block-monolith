import pandas as pd
from data_blocks.blocks.crypto_data.alpha_vantage import get_crypto_data


def run(input):
    """
    Runs a query to get the crypto data

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
            return "W"
        elif case("1month"):
            return "M"

    response_df = get_crypto_data(input["crypto_name"], input["candlestick"])

    date_range = pd.date_range(
        input["start_date"],
        input["end_date"],
        freq=map_candlestick_to_freq_date(input["candlestick"]),
    )

    date_intersection = date_range.intersection(response_df.index)

    merged_df = pd.DataFrame(response_df, index=date_intersection)

    # Converts to JSON
    merged_df = merged_df.sort_index()
    merged_df["timestamp"] = merged_df.index.values.astype(str)
    response_dict = {"response": merged_df.to_dict(orient="records")}

    return response_dict
