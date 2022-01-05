import pandas as pd
from django.test import TestCase
from pandas.util.testing import assert_frame_equal
from pydantic import BaseModel, StrictStr

from utils.exceptions import (
    BlockDataDoesNotExistException,
    BlockDoesNotExistException,
    FieldDoesNotExistException,
    InvalidRequestException,
    KeyDoesNotExistException,
)
from utils.utils import (
    format_computational_block_response,
    format_request,
    format_signal_block_response,
    get_data_from_id_and_field,
    retrieve_block_data,
    validate_payload,
)


class TestFormatRequest(TestCase):
    def test_empty_request_json_raises_exception(self):
        with self.assertRaises(InvalidRequestException):
            format_request(None, "timestamp")

    def test_empty_array_request_json_raises_exception(self):
        with self.assertRaises(InvalidRequestException):
            format_request([], "timestamp")

    def test_key_does_not_exist_in_json(self):
        with self.assertRaises(KeyDoesNotExistException):
            format_request([{"value": 0, "data": 0}], "timestamp")

    def test_successfully_returns_request_df(self):
        response_df = format_request(
            [{"timestamp": "01/31/2021", "data": 0.00}], "timestamp"
        )
        expected_response_df = pd.DataFrame(
            [["01/31/2021", 0.00]], columns=["timestamp", "data"]
        )
        expected_response_df = expected_response_df.set_index("timestamp")

        assert_frame_equal(response_df, expected_response_df)


class FormatComputationalBlockResponse(TestCase):
    def test_ok(self):
        response_df = pd.DataFrame(
            [["01/31/2021", 0.00]], columns=["timestamp", "data"]
        )
        response_df = response_df.set_index("timestamp")
        response_json = format_computational_block_response(
            response_df, "timestamp", "data"
        )

        self.assertEqual(response_json, [{"timestamp": "01/31/2021", "data": 0.0}])


class FormatSignalBlockResponse(TestCase):
    def test_ok(self):
        response_df = pd.DataFrame(
            [["01/31/2021", "BUY"]], columns=["timestamp", "order"]
        )
        response_df = response_df.set_index("timestamp")

        response_json = format_signal_block_response(
            response_df, "timestamp", ["order"]
        )

        self.assertEqual(response_json, [{"timestamp": "01/31/2021", "order": "BUY"}])


class TestRetrieveBlockData(TestCase):
    def test_single_block_ok(self):
        selectable_data = {"data_block": ["DATA_BLOCK"]}
        incoming_data = {"DATA_BLOCK": []}

        response = retrieve_block_data(selectable_data, incoming_data)

        self.assertDictEqual(response, {"data_block": []})

    def test_multiple_block_ok(self):
        selectable_data = {
            "data_block": ["DATA_BLOCK"],
            "signal_block": ["SIGNAL_BLOCK"],
        }
        incoming_data = {"DATA_BLOCK": [], "SIGNAL_BLOCK": []}

        response = retrieve_block_data(selectable_data, incoming_data)

        self.assertDictEqual(response, {"data_block": [], "signal_block": []})

    def test_raises_exception_when_block_not_found(self):
        selectable_data = {
            "data_block": ["DATA_BLOCK"],
            "signal_block": ["SIGNAL_BLOCK"],
        }
        incoming_data = {"DATA_BLOCK": []}

        with self.assertRaises(BlockDataDoesNotExistException):
            retrieve_block_data(selectable_data, incoming_data)


class TestGetDataFromIdAndField(TestCase):
    output = {
        "COMPUTATIONAL_BLOCK-1-2": [
            {"timestamp": "01/01/2020", "close": "12.00"},
            {"timestamp": "01/02/2020", "close": "12.00"},
            {"timestamp": "01/03/2020", "close": "12.00"},
            {"timestamp": "01/04/2020", "close": "12.00"},
            {"timestamp": "01/05/2020", "close": "15.00"},
        ],
    }

    def test_success_return_df(self):
        data = get_data_from_id_and_field("2-close", self.output)
        expected_df = pd.DataFrame(
            {"data": ["12.00", "12.00", "12.00", "12.00", "15.00"]},
            index=[
                "01/01/2020",
                "01/02/2020",
                "01/03/2020",
                "01/04/2020",
                "01/05/2020",
            ],
        )
        expected_df.index.name = "timestamp"
        assert_frame_equal(data, expected_df)

    def test_failure_error_non_existing_block_id(self):
        with self.assertRaises(BlockDoesNotExistException):
            get_data_from_id_and_field("3-close", self.output)

    def test_failure_error_non_existing_field(self):
        with self.assertRaises(FieldDoesNotExistException):
            get_data_from_id_and_field("2-test", self.output)


class TestValidatePayload(TestCase):
    class InputPayload(BaseModel):
        foo: str
        bar: StrictStr
        foobar: int

    class CustomException(Exception):
        pass

    def test_ok(self):
        input = validate_payload(
            self.InputPayload,
            {"foo": "foo_str", "bar": "bar_str", "foobar": 1},
            Exception,
        )
        self.assertEqual(
            input, self.InputPayload(foo="foo_str", bar="bar_str", foobar=1)
        )

    def test_success_casted_type(self):
        input = validate_payload(
            self.InputPayload, {"foo": 5, "bar": "bar_str", "foobar": "1"}, Exception
        )
        self.assertEqual(input, self.InputPayload(foo="5", bar="bar_str", foobar=1))

    def test_failure_strict_type(self):
        with self.assertRaises(self.CustomException) as ctx:
            input = validate_payload(
                self.InputPayload,
                {"foo": "foo_str", "bar": 5, "foobar": "1"},
                self.CustomException,
            )
        self.assertEqual(
            str(ctx.exception),
            '[\n  {\n    "loc": [\n      "bar"\n    ],\n    "msg": "str type expected",\n    "type": "type_error.str"\n  }\n]',
        )

    def test_failure_missing_variable_and_strict_type(self):
        with self.assertRaises(self.CustomException) as ctx:
            input = validate_payload(
                self.InputPayload, {"foo": "foo_str", "bar": 5}, self.CustomException
            )
        self.assertEqual(
            str(ctx.exception),
            '[\n  {\n    "loc": [\n      "bar"\n    ],\n    "msg": "str type expected",\n    "type": "type_error.str"\n  },\n  {\n    "loc": [\n      "foobar"\n    ],\n    "msg": "field required",\n    "type": "value_error.missing"\n  }\n]',
        )

    def test_failure_missing_variable_custom_text(self):
        with self.assertRaises(self.CustomException) as ctx:
            input = validate_payload(
                self.InputPayload,
                {"foo": "foo_str", "bar": 5},
                self.CustomException,
                "my custom exception",
            )
        self.assertEqual(str(ctx.exception), "my custom exception")
