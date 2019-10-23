import os
from gym.envs.registration import register

filepath = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(filepath, 'data')

# Currency to trade in the environment
currency = 'BTC'

# Total capital at the start of trading
capital = 1000

# Granularity of trading
granularity = '30min'

#Transaction percentage cost
transaction_pct = 0.005


kwargs = {'currency': currency, 'granularity':granularity, 'capital':capital, 'transaction_pct':transaction_pct,
          'data_path':data_path}

register(id='crypto-gym-v0', entry_point='gym_crypto.envs:CryptoEnv', kwargs=kwargs.copy())