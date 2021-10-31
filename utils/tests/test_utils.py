import pandas as pd
from django.test import TestCase
from pandas.util.testing import assert_frame_equal

from utils.exceptions import InvalidRequestException, KeyDoesNotExistException
from utils.utils import format_request, get_data_from_id_and_field


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
            [{"timestamp": "2020-01-01", "data": 0.00}], "timestamp"
        )
        expected_response_df = pd.DataFrame(
            [["2020-01-01", 0.00]], columns=["timestamp", "data"]
        )
        expected_response_df = expected_response_df.set_index("timestamp")

        assert_frame_equal(response_df, expected_response_df)


class TestUtils(TestCase):
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
        # TODO
        pass

    def test_failure_error_non_existing_field(self):
        # TODO
        pass
