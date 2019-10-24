import pandas as pd
from unittest import TestCase
from gym_crypto.data_utils.data_utils import get_avaliable_currencies, read_data

class TestGet_avaliable_currencies(TestCase):
    def test_get_avaliable_currencies(self):
        currencies = get_avaliable_currencies()
        self.assertIsNotNone(currencies)

class TestRead_original_data(TestCase):
    def test_read_data(self):
        data = read_data('BTC')
        self.assertIsInstance(data, pd.DataFrame)
