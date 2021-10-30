from signal_blocks.crossover_block.events.crossover_above import (
    main as crossover_above,
)
from signal_blocks.crossover_block.events.crossover_below import (
    main as crossover_below,
)
from utils.utils import get_data_from_id_and_field


def run(input, output):
    """
    Takes in elements from the form input and a single COMPUTATIONAL_BLOCK
    to generates a series of events associated with that block

    Attributes
    ----------
    input: Form Inputs
    computational_block: Time series data from a computational block
    """

    data_field_string = input.get("incoming_data")

    # TODO: VALIDATION
    if data_field_string is None:
        pass

    computational_block_df = get_data_from_id_and_field(data_field_string, output)

    _crossover_func = None
    case = lambda x: x == input["event_type"]

    if case("ABOVE"):
        _crossover_func = crossover_above
    elif case("BELOW"):
        _crossover_func = crossover_below

    response_df = _crossover_func(
        computational_block_df,
        input["event_action"],
        crossover_value=float(input["event_value"]),
    )
    return _format_response(response_df)


def _format_response(response_df):
    response_df = response_df.reset_index(level="timestamp")
    response_df.drop(
        response_df.columns.difference(["timestamp", "order"]), 1, inplace=True
    )
    response_df = response_df.dropna()
    response_json = response_df.to_dict(orient="records")
    return response_json
