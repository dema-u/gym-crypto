import os
import pandas as pd
from gym_crypto import DATA_PATH

def read_data(currency):
    data = pd.read_csv('{}\\{}.csv'.format(DATA_PATH, currency), index_col='Date')
    return data

def get_avaliable_currencies():

    all_files = os.listdir(DATA_PATH)
    currencies = [currency.strip('.csv') for currency in all_files]

    return currencies