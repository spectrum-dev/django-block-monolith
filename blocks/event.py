import computational_blocks.views
import signal_blocks.views
import strategy_blocks.views
import data_blocks.views


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

    input = payload.get("input", {})
    output = payload.get("output", {})

    case = lambda x: x == block_type

    if case("DATA_BLOCK"):
        if block_id == 1:
            return data_blocks.views.us_stock_data_run(input)
        elif block_id == 2:
            return data_blocks.views.crypto_run(input)

    elif case("COMPUTATIONAL_BLOCK"):
        if block_id == 1:
            return computational_blocks.views.process_technical_analysis_run(
                input, output
            )

    elif case("SIGNAL_BLOCK"):
        if block_id == 1:
            return signal_blocks.views.signal_block_run(input, output)
        elif block_id == 2:
            return signal_blocks.views.saddle_block_run(input, output)
        elif block_id == 3:
            return signal_blocks.views.and_run(output)
        elif block_id == 4:
            return signal_blocks.views.crossover_block_run(input, output)
        elif block_id == 5:
            return signal_blocks.views.or_run(output)
        elif block_id == 6:
            pass

    elif case("STRATEGY_BLOCK"):
        if block_id == 1:
            return strategy_blocks.views.process_post_run(input, output)

    else:
        pass
