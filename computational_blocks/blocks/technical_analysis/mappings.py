# TODO: Talk with Ronak to see if we should start putting these things in the database
INDICATORS = {
    "MA": {
        "shortName": "MA",
        "longName": "Simple Moving Average",
        "functionName": "moving_average",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",  # DESCRIPTIONS["lookbackPeriod"]
                "default": 10,
            }
        ],
    },
    "EMA": {
        "shortName": "EMA",
        "longName": "Exponential Moving Average",
        "functionName": "exponential_moving_average",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "MACD": {
        "shortName": "MACD",
        "longName": "Moving Average Convergence Divergence",
        "functionName": "macd",
        "params": [
            {
                "name": "Lookback Period One",
                "internalName": "lookback_period_one",
                "description": "",
                "default": 10,
            },
            {
                "name": "Lookback Period Two",
                "internalName": "lookback_period_two",
                "description": "",
                "default": 10,
            },
        ],
    },
    "ADX": {
        "shortName": "ADX",
        "longName": "Average Directional Movement Index",
        "functionName": "adx",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "ADXR": {
        "shortName": "ADXR",
        "longName": "Average Directional Movement Index Rating",
        "functionName": "adxr",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "APO": {
        "shortName": "APO",
        "longName": "Absolute Price Oscillator",
        "functionName": "apo",
        "params": [
            {
                "name": "Fast Period",
                "internalName": "fast_period",
                "description": "",
                "default": 10,
            },
            {
                "name": "Slow Period",
                "internalName": "slow_period",
                "description": "",
                "default": 10,
            },
            {
                "name": "MA Type",
                "internalName": "ma_type",
                "description": "",
                "default": 10,
            },
        ],
    },
    "AROONOSC": {
        "shortName": "AROONOSC",
        "longName": "Aroon Oscillator",
        "functionName": "aroon_oscillator",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "BOP": {
        "shortName": "BOP",
        "longName": "Balance Of Power",
        "functionName": "bop",
        "params": [],
    },
    "CCI": {
        "shortName": "CCI",
        "longName": "Commodity Channel Index",
        "functionName": "cci",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "CMO": {
        "shortName": "CMO",
        "longName": "Chande Momentum Oscillator",
        "functionName": "cmo",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "DX": {
        "shortName": "DX",
        "longName": "Directional Movement Index",
        "functionName": "dx",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "RSI": {
        "shortName": "RSI",
        "longName": "Relative Strength Index",
        "functionName": "rsi",
        "params": [
            {
                "name": "Lookback Period",
                "internalName": "lookback_period",
                "description": "",
                "default": 10,
            }
        ],
    },
    "BB": {
        "shortName": "BB",
        "longName": "Bollinger Bands %B (<0 is below lower bound and >1 is above upper bound)",
        "functionName": "bb",
        "params": [],
    },
    "DB": {
        "shortName": "DB",
        "longName": "Donchian Bands %B (similar to BB but uses low and high of period)",
        "functionName": "db",
        "params": [],
    },
    "KAMA": {
        "shortName": "KAMA",
        "longName": "KAMA Indicator",
        "functionName": "kama",
        "params": [],
    },
    "KC": {
        "shortName": "KC",
        "longName": "Keltner Channel",
        "functionName": "kc",
        "params": [],
    },
    "MI": {
        "shortName": "MI",
        "longName": "Mass Index (fluctuates around 20)",
        "functionName": "mi",
        "params": [],
    },
    "STOC_OSCI": {
        "shortName": "STOC_OSCI",
        "longName": "Stochastic Oscillator",
        "functionName": "stoc_osci",
        "params": [],
    },
    "TRIX": {
        "shortName": "TRIX",
        "longName": "Triple Smoothed SMA Rate of Change",
        "functionName": "trix",
        "params": [],
    },
    "TSI": {
        "shortName": "TSI",
        "longName": "True Strength Index",
        "functionName": "tsi",
        "params": [],
    },
}
