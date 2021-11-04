import operator

from pydantic import BaseModel

from utils.utils import (
    format_computational_block_response,
    format_request,
    retrieve_block_data,
)

from .exceptions import (
    DataValueNotFloatException,
    FieldDoesNotExistException,
    InvalidOperationTypeException,
    OperationValueNotFloatException,
)


class InputPayload(BaseModel):
    data_field: str
    operation_value: str
    operation_type: str


def run(input, output):
    """
    Takes in elements from the form input, and a DATA_BLOCK or COMPUTATIONAL_BLOCK to apply some mathematical operation on a chosen field.

    Attributes
    ----------
    input: Form inputs provided in metadata
    output: Data from a data_block or computational_block stream (has to be numeric so to apply mathematical operation on)
    """

    selectable_data = {
        "data_or_computational_block": [
            "DATA_BLOCK",
            "BULK_DATA_BLOCK",
            "COMPUTATIONAL_BLOCK",
        ]
    }
    block_data = retrieve_block_data(selectable_data, output)

    input = InputPayload(**input)
    data_field = input.data_field
    try:
        operation_value = float(input.operation_value)
    except ValueError:
        raise OperationValueNotFloatException
    case = lambda x: x == input.operation_type
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
    else:
        raise InvalidOperationTypeException

    data_block_df = format_request(
        block_data["data_or_computational_block"], "timestamp"
    )

    if data_field not in data_block_df.columns:
        raise FieldDoesNotExistException

    try:
        operation_lhs = data_block_df[data_field].astype(float)
    except ValueError:
        raise DataValueNotFloatException

    data_block_df["data"] = operator_func(operation_lhs, operation_value)

    return {
        "response": format_computational_block_response(
            data_block_df[["data"]], "timestamp", "data"
        )
    }
