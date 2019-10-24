import os
from gym.envs.registration import register

filepath = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(filepath, 'data')

kwargs = {'data_path':DATA_PATH}

register(id='gym-crypto-v0', entry_point='gym_crypto.envs:CryptoEnv', kwargs=kwargs.copy())
