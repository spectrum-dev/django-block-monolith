INDICATORS = {
    "MA": {
        "shortName": "MA",
        "longName": "Simple Moving Average",
        "functionName": "moving_average",
        "params": [
            {
                "fieldName": "Lookback Period",
                "fieldVariableName": "lookback_period",
                "fieldType": "input",
            }
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
}
