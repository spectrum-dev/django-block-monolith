import pandas as pd
import ta
from talib import ADX, ADXR, APO, AROONOSC, BOP, CCI, CMO, DX, EMA, RSI

"""
    Documentation
    ---
    https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
"""


def moving_average(
    data_block=None,
    incoming_data="close",
    lookback_period="20",
    lookback_unit="DATA_POINT",
):
    """
    Implementation of a simple moving average strategy with a variable
    time period in the calculation
    data_block          :   Data corresponding to price data
    lookback_data_type  :   Data Type from Lookback
    lookback_period     :   Time Period of Rolling Average
    lookback_unit       :   Unit of How Looking Back
    """
    rolling_average = (
        data_block[incoming_data].rolling(window=int(lookback_period)).mean()
    )

    return rolling_average


def exponential_moving_average(
    data_block=None,
    lookback_data_type="close",
    lookback_period="20",
    lookback_unit="DATA_POINT",
):
    """
    Implementation of an exponential moving average strategy with
    a variable time period in the calculation

    data                :   Data corresponding to price data
    time_period         :   TBD
    Takes simple average for first N lookback_period as starting point of Nth EMA.
    """

    ema = EMA(data_block[lookback_data_type], timeperiod=int(lookback_period))

    return ema


def macd(
    data_block=None,
    lookback_data_type="close",
    lookback_period_one="12",
    lookback_period_two="26",
    lookback_unit="DATA_POINT",
):
    """
    Implementation of the moving average converdence divergence indicator
    https://www.investopedia.com/terms/m/macd.asp
    data_block                    :   Data corresponding to price data
    lookback_period_one     :   TBD
    lookback_period_two     :   TBD
    """

    macd = exponential_moving_average(
        data_block=data_block,
        lookback_data_type=lookback_data_type,
        lookback_period=lookback_period_one,
        lookback_unit=lookback_unit,
    ) - exponential_moving_average(
        data_block=data_block,
        lookback_data_type=lookback_data_type,
        lookback_period=lookback_period_two,
        lookback_unit=lookback_unit,
    )

    return macd


def adx(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ADX(
        data_block["high"],
        data_block["low"],
        data_block["close"],
        timeperiod=int(lookback_period),
    )

    return response


def adxr(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ADXR(
        data_block["high"],
        data_block["low"],
        data_block["close"],
        timeperiod=int(lookback_period),
    )

    return response


def apo(
    data_block=None,
    fast_period="12",
    slow_period="12",
    ma_type="0",
    lookback_unit="DATA_POINT",
):
    response = APO(
        data_block["close"],
        fastperiod=int(fast_period),
        slowperiod=int(slow_period),
        matype=int(ma_type),
    )

    return response


def aroon_oscillator(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = AROONOSC(
        data_block["high"], data_block["low"], timeperiod=int(lookback_period)
    )

    return response


def bop(data_block=None):
    response = BOP(
        data_block["open"], data_block["high"], data_block["low"], data_block["close"]
    )

    return response


def cci(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = CCI(
        data_block["high"],
        data_block["low"],
        data_block["close"],
        timeperiod=int(lookback_period),
    )

    return response


def cmo(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = CMO(data_block["close"], timeperiod=int(lookback_period))

    return response


def dx(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = DX(
        data_block["high"],
        data_block["low"],
        data_block["close"],
        timeperiod=int(lookback_period),
    )

    return response


def rsi(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = RSI(data_block["close"], timeperiod=int(lookback_period))

    return response


def bb(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.volatility.bollinger_pband(
        close=data_block["close"].astype(float), fillna=True
    )

    return response


def db(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.volatility.donchian_channel_pband(
        high=data_block["high"].astype(float),
        low=data_block["low"].astype(float),
        close=data_block["close"].astype(float),
        fillna=True,
    )

    return response


def kama(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.momentum.kama(close=data_block["close"].astype(float), fillna=True)

    return response


def kc(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.volatility.keltner_channel_pband(
        high=data_block["high"].astype(float),
        low=data_block["low"].astype(float),
        close=data_block["close"].astype(float),
        fillna=True,
    )

    return response


def mi(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.trend.mass_index(
        high=data_block["high"].astype(float),
        low=data_block["low"].astype(float),
        fillna=True,
    )

    return response


def stoch_osci(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.momentum.stoch(
        close=data_block["close"].astype(float),
        high=data_block["high"].astype(float),
        low=data_block["low"].astype(float),
    )

    return response


def trix(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.trend.trix(close=data_block["close"].astype(float), fillna=True)

    return response


def tsi(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    response = ta.momentum.tsi(close=data_block["close"].astype(float), fillna=True)

    return response


def opening_range(data_block=None, lookback_period="20", lookback_field="high"):
    """
    Implementation of an intrday opening range strategy. Takes in first N lookback_period of each day and compute either
    low/high/mid of that period and return it as a static value for the entire day.
    Main idea here is, for example, to get a knowledge of the high of first 30 bars of each day.
    data_block          :   Data corresponding to price data
    lookback_period     :   Number of periods to compute range
    lookback_field      :   low/high/mid to compute different range statistics of time period
    """
    assert lookback_field in ["high", "low", "mid"]
    # Convert to proper datetime column since we need to compute on date
    data_block.index = pd.to_datetime(data_block.index)
    data_block["high"] = data_block["high"].astype(float)
    data_block["low"] = data_block["low"].astype(float)
    # We make a date-level column to group since opening range is necessarily intraday
    data_block["datestamp"] = data_block.index.date
    # Keep top-N periods per day for opening range
    # TODO: flexible range, probably use datetime to subset for certain time period range
    df_subset = data_block.groupby(["datestamp"]).head(int(lookback_period))
    opening_range_period = list(df_subset.index)
    df_stats = (
        df_subset.groupby(["datestamp"])
        .agg(high=("high", max), low=("low", min))
        .reset_index()
    )
    df_stats["mid"] = (df_stats["high"] + df_stats["low"]) / 2
    # Rename target column with 'data' as expected by downstream processes
    df_stats = df_stats.rename(columns={lookback_field: "data"})
    output = data_block[["datestamp"]]
    # Merge back onto initial data with 1 row per candle
    output = (
        output.reset_index()
        .merge(df_stats[["datestamp", "data"]], how="left", on="datestamp")
        .set_index("timestamp")
    )
    # Make rows of data within opening range None since we don't want to have look-ahead bias
    output["data"] = [
        output["data"][x] if output.index[x] not in opening_range_period else None
        for x in range(len(output))
    ]
    del output["datestamp"]

    return output
