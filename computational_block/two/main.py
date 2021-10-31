import operator

from utils.utils import format_computational_block_response, format_request


def run(input, output):
    """
    Takes in elements from the form input, and a DATA_BLOCK or COMPUTATIONAL_BLOCK to apply some mathematical operation on a chosen field.

    Attributes
    ----------
    input: Form inputs provided in metadata
    output: Data from a data_block or computational_block stream (has to be numeric so to apply mathematical operation on)
    """

    data_block = None
    for key in output.keys():
        key_breakup = key.split("-")
        if (
            key_breakup[0] == "DATA_BLOCK"
            or key_breakup[0] == "BULK_DATA_BLOCK"
            or key_breakup[0] == "COMPUTATIONAL_BLOCK"
        ):
            data_block = output[key]
            break

    data_field = input["data_field"]
    operation_value = input["operation_value"]
    case = lambda x: x == input["operation_type"]
    if case("+"):
        operator_func = operator.add
    elif case("-"):
        operator_func = operator.sub
    elif case("*"):
        operator_func = operator.mul
    elif case("/"):
        operator_func = operator.truediv
    elif case("^"):
        operator_func = operator.pow

    data_block_df = format_request(data_block, "timestamp")
    data_block_df["data"] = operator_func(
        data_block_df[data_field].astype(float), float(operation_value)
    )
    return {
        "response": format_computational_block_response(
            data_block_df[["data"]], "timestamp", "data"
        )
    }
