import talib
import pandas as pd

from talib import EMA, ADX, ADXR, APO, AROON, AROONOSC, BOP, CCI, CMO, DX, RSI

"""
    Documentation
    ---
    https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
"""


def moving_average(
    data_block=None,
    lookback_data_type="close",
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
        data_block[lookback_data_type].rolling(window=int(lookback_period)).mean()
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


def aroon(data_block=None, lookback_period="20", lookback_unit="DATA_POINT"):
    aroondown, aroonup = AROON(
        data_block["high"], data_block["low"], timeperiod=int(lookback_period)
    )

    # TODO: Determine what to return
    return


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
