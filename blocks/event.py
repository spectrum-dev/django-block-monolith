# Data Blocks
from data_blocks.blocks.us_stock_data.main import run as data_block_1_run
from data_blocks.blocks.crypto_data.main import run as data_block_2_run

# Computational Blocks
from computational_blocks.blocks.technical_analysis.main import (
    run as computational_block_1_run,
)

# Signal Blocks
from signal_blocks.blocks.intersect_block.main import run as signal_block_1_run
from signal_blocks.blocks.saddle_block.main import run as signal_block_2_run
from signal_blocks.blocks.and_block.main import run as signal_block_3_run
from signal_blocks.blocks.crossover_block.main import run as signal_block_4_run
from signal_blocks.blocks.or_block.main import run as signal_block_5_run
from signal_blocks.blocks.candle_close_block.main import run as signal_block_6_run

# Strategy Blocks
from strategy_blocks.blocks.simple_backtest.main import run as strategy_block_1_run


def event_ingestor(payload):
    """
    Takes in a payload resembling:

    {
        "blockType": "",
        "blockId": "",
        "inputs": { ... },
        "outputs": { ... }
    }
    """
    block_type = payload.get("blockType", "DNE")
    block_id = payload.get("blockId", -1)

    inputs = payload.get("inputs", {})
    outputs = payload.get("outputs", {})

    case = lambda x: x == block_type

    if case("DATA_BLOCK"):
        if block_id == 1:
            return data_block_1_run(inputs)
        elif block_id == 2:
            return data_block_2_run(inputs)

    elif case("COMPUTATIONAL_BLOCK"):
        if block_id == 1:
            return computational_block_1_run(inputs, outputs)

    elif case("SIGNAL_BLOCK"):
        if block_id == 1:
            return signal_block_1_run(inputs, outputs)
        elif block_id == 2:
            return signal_block_2_run(inputs, outputs)
        elif block_id == 3:
            return signal_block_3_run(outputs)
        elif block_id == 4:
            return signal_block_4_run(inputs, outputs)
        elif block_id == 5:
            return signal_block_5_run(outputs)
        elif block_id == 6:
            return signal_block_6_run(inputs, outputs)

    elif case("STRATEGY_BLOCK"):
        if block_id == 1:
            return strategy_block_1_run(inputs, outputs)

    raise Exception("Block type or ID is invalid")
