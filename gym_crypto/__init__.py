import os
from gym.envs.registration import register

filepath = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(filepath, 'data')

kwargs = {'data_path':data_path}

register(id='gym-crypto-v0', entry_point='gym_crypto.envs:CryptoEnv', kwargs=kwargs.copy())