import operator

from pydantic import BaseModel

from utils.utils import (
    format_computational_block_response,
    format_request,
    retrieve_block_data,
    validate_payload,
)

from .exceptions import (
    ComputationalBlockTwoDataValueNotFloatException,
    ComputationalBlockTwoFieldDoesNotExistException,
    ComputationalBlockTwoInputPayloadInvalidException,
    ComputationalBlockTwoInvalidOperationTypeException,
    ComputationalBlockTwoOperationValueNotFloatException,
)


class InputPayload(BaseModel):
    data_field: str
    operation_value: str
    operation_type: str


def run(input: dict, output: dict) -> dict:
    """
    Operation Block: Generate signals based on mathematical operations on a
    chosen field

    Args:
        input (dict): Input payload from flow
        output (dict): Data payload from DATA_BLOCK or COMPUTATIONAL_BLOCK

    Raises:
        ComputationalBlockTwoOperationValueNotFloatException: Named exception raised
            when operation_value supplied cannot be converted to float
        ComputationalBlockTwoInvalidOperationTypeException: Named exception raised
            when unsupported operation_type is supplied
        ComputationalBlockTwoFieldDoesNotExistException: Named exception raised
            when data_field does not exist in supplied data
        ComputationalBlockTwoDataValueNotFloatException: Named exception raised
            when data_field cannot be converted to float

    Returns:
        dict: JSON representation of computed dataframe
    """

    selectable_data = {
        "data_or_computational_block": [
            "DATA_BLOCK",
            "BULK_DATA_BLOCK",
            "COMPUTATIONAL_BLOCK",
        ]
    }
    block_data = retrieve_block_data(selectable_data, output)

    input = validate_payload(
        InputPayload, input, ComputationalBlockTwoInputPayloadInvalidException
    )
    data_field = input.data_field
    try:
        operation_value = float(input.operation_value)
    except ValueError:
        raise ComputationalBlockTwoOperationValueNotFloatException
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
        raise ComputationalBlockTwoInvalidOperationTypeException

    data_block_df = format_request(
        block_data["data_or_computational_block"], "timestamp"
    )

    if data_field not in data_block_df.columns:
        raise ComputationalBlockTwoFieldDoesNotExistException

    try:
        operation_lhs = data_block_df[data_field].astype(float)
    except ValueError:
        raise ComputationalBlockTwoDataValueNotFloatException

    data_block_df["data"] = operator_func(operation_lhs, operation_value)

    return {
        "response": format_computational_block_response(
            data_block_df[["data"]], "timestamp", "data"
        )
    }
