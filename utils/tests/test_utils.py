import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from utils.utils import get_data_from_id_and_field


class TestUtils(unittest.TestCase):
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
