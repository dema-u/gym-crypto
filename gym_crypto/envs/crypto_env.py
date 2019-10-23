import gym
import numpy as np
import pandas as pd
from gym import spaces
from gym.utils import seeding


class CryptoEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):

        self.data_path = kwargs['data_path']

        self.currency = kwargs['currency']
        self.granularity = kwargs['granularity']
        self.transaction_pct = kwargs['transaction_pct']
        self.capital = kwargs['capital']

        self.full_data, self.crypto_returns, self.dates = self.configure_currency(self.currency)

        observation_range = np.finfo('float32').min, np.finfo('float32').max
        weight_range = -1.0, 1.0

        ohclv_space = spaces.Box(*observation_range, (1,))
        capital_space = spaces.Box(*observation_range, (1,))
        weight_space = spaces.Box(*weight_range, (1,))

        self.observation_space = spaces.Tuple((ohclv_space, capital_space, weight_space))
        self.action_space = spaces.Box(*weight_range, [len(self.currency)])

        self.total_capital_history = None
        self.capital_exposure_history = None
        self.weight_history = None
        self.returns_history = None
        self.tcosts_history = None

        self.index = None
        self.start_index = None
        self.end_index = None

        self.set_simulation_window(0, len(self.full_data))

    def step(self, capital_weight):

        capital_exposure = self.total_capital_history[-1]*capital_weight
        transaction_costs = np.abs(self.capital_exposure_history[-1]-capital_exposure)*self.transaction_pct

        self.index += 1

        returns = self.crypto_returns[self.index] * capital_exposure
        total_returns = returns - transaction_costs

        self.total_capital_history.append(self.total_capital_history[-1]+total_returns)
        self.capital_exposure_history.append(capital_exposure)
        self.weight_history.append(capital_weight)
        self.returns_history.append(returns)
        self.tcosts_history.append(transaction_costs)

        observation = self._get_observation()
        done = True if (self.index == self.end_index - 1) else False
        reward = total_returns

        return observation, reward, done, {}

    def reset(self):

        self.done = False
        self.index = self.start_index
        self._reset_history()

        observation = self._get_observation()

        return observation, {}

    def render(self, mode='human', close=False):
        returns = (np.array(self.tcosts_history) + np.array(self.returns_history)).tolist()
        return returns[1:], self.weight_history[1:]

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def set_simulation_window(self, start_index, end_index):

        self.start_index = start_index
        self.end_index = end_index

        self.reset()

    def configure_currency(self, currency):

        full_path = '{}\\{}.csv'.format(self.data_path, currency)
        full_data = pd.read_csv(full_path, index_col='Date')

        full_data_price = full_data['{}.close'.format(currency)]
        full_data_return = full_data_price.pct_change().fillna(0).values

        dates = full_data.index

        return full_data, full_data_return, dates

    def _get_observation(self):

        ohlcv = self.full_data.iloc[self.index].values
        capital = self.total_capital_history[-1]
        weight = self.weight_history[-1]

        return (ohlcv, capital, weight)

    def _reset_history(self):

        self.total_capital_history = [self.capital]
        self.capital_exposure_history = [0]
        self.weight_history = [0]
        self.returns_history = [0]
        self.tcosts_history = [0]

    def _get_crypto_returns(self):

        crypto_price = self.full_data['{}.close'.format(self.currency)]
        crypto_returns = crypto_price.pct_change().fillna(0).values

        return crypto_returns