from django.test import TestCase

from data_store.interface import store_eod_data

# Create your tests here.


class TestStoreEodData(TestCase):
    def test_debug(self):
        store_eod_data("2021-01-01", "2021-02-02")
