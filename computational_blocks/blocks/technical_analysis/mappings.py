INDICATORS = {
    "MA": {
        "shortName": "MA",
        "longName": "Simple Moving Average",
        "functionName": "moving_average",
        "params": [
            {
                "fieldName": "Incoming Data",
                "fieldVariableName": "incoming_data",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            },
        ],
    },
    "EMA": {
        "shortName": "EMA",
        "longName": "Exponential Moving Average",
        "functionName": "exponential_moving_average",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "MACD": {
        "shortName": "MACD",
        "longName": "Moving Average Convergence Divergence",
        "functionName": "macd",
        "params": [
            {
                "fieldName": "Lookback Period One",
                "fieldVariableName": "lookback_period_one",
                "fieldType": "input",
            },
            {
                "fieldName": "Lookback Period Two",
                "fieldVariableName": "lookback_period_two",
                "fieldType": "input",
            },
        ],
    },
    "ADX": {
        "shortName": "ADX",
        "longName": "Average Directional Movement Index",
        "functionName": "adx",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "ADXR": {
        "shortName": "ADXR",
        "longName": "Average Directional Movement Index Rating",
        "functionName": "adxr",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "APO": {
        "shortName": "APO",
        "longName": "Absolute Price Oscillator",
        "functionName": "apo",
        "params": [
            {
                "fieldName": "Fast Period",
                "fieldVariableName": "fast_period",
                "fieldType": "input",
            },
            {
                "fieldName": "Slow Period",
                "fieldVariableName": "slow_period",
                "fieldType": "input",
            },
            {
                "fieldName": "MA Type",
                "fieldVariableName": "ma_type",
                "fieldType": "input",
            },
        ],
    },
    "AROONOSC": {
        "shortName": "AROONOSC",
        "longName": "Aroon Oscillator",
        "functionName": "aroon_oscillator",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
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
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "CMO": {
        "shortName": "CMO",
        "longName": "Chande Momentum Oscillator",
        "functionName": "cmo",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "DX": {
        "shortName": "DX",
        "longName": "Directional Movement Index",
        "functionName": "dx",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
        ],
    },
    "RSI": {
        "shortName": "RSI",
        "longName": "Relative Strength Index",
        "functionName": "rsi",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
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
    "STOCH_OSCI": {
        "shortName": "STOCH_OSCI",
        "longName": "Stochastic Oscillator",
        "functionName": "stoch_osci",
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
    "OR": {
        "shortName": "OR",
        "longName": "Opening Range",
        "functionName": "opening_range",
        "params": [
            {
                "fieldName": "Opening Range Type",
                "fieldVariableName": "lookback_field",
                "fieldType": "input",  # low/high (must be in data block)
            },
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            },
        ],
    },
}
