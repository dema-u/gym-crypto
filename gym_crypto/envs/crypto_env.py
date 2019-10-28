import gym
import numpy as np
import pandas as pd
from gym import spaces
from gym.utils import seeding


class CryptoEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, **kwargs):

        self.data_path = kwargs['data_path']

        self.configuration = None

        self._currency = None
        self._granularity = None
        self._transaction_pct = None
        self._capital = None

        self._full_data = None
        self._crypto_returns = None
        self._dates = None

        observation_range = np.finfo('float32').min, np.finfo('float32').max
        weight_range = -1.0, 1.0

        ohclv_space = spaces.Box(*observation_range, (1,))
        capital_space = spaces.Box(*observation_range, (1,))
        weight_space = spaces.Box(*weight_range, (1,))

        self.observation_space = spaces.Tuple((ohclv_space, capital_space, weight_space))
        self.action_space = spaces.Box(*weight_range, (1,))

        self.total_capital_history = None
        self.capital_exposure_history = None
        self.weight_history = None
        self.returns_history = None
        self.tcosts_history = None

        self.index = None
        self.start_index = None
        self.end_index = None

    def step(self, capital_weight):

        capital_exposure = self.total_capital_history[-1]*capital_weight
        transaction_costs = np.abs(self.capital_exposure_history[-1]-capital_exposure)*self._transaction_pct

        self.index += 1

        returns = self._crypto_returns[self.index] * capital_exposure
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

    def _set_simulation_window(self, start_date, end_date):

        self.start_index = self._dates[self._dates == start_date].index.item()
        self.end_index = self._dates[self._dates == end_date].index.item()

        self.reset()

    def configure_env(self, **config):

        self.currency = config['currency']
        self.granularity = config['granularity']
        self.transaction_pct = config['transaction_pct']
        self.capital = config['capital']

        self._set_simulation_window(config['start_date'], config['end_date'])

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, currency):
        self._currency = currency

        full_path = '{}\\{}.csv'.format(self.data_path, currency)
        self._full_data = pd.read_csv(full_path, index_col='Date')
        self._full_data.index = pd.to_datetime(self._full_data.index)
        self._dates = pd.Series(self._full_data.index)

        full_data_price = self._full_data['{}.close'.format(currency)]
        self._crypto_returns = full_data_price.pct_change().fillna(0).values

    @property
    def granularity(self):
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        if granularity != '30min':
            raise NotImplementedError('Only 30min granularity is implemented so far.')
        else:
            self._granularity = granularity

    @property
    def transaction_pct(self):
        return self._transaction_pct

    @transaction_pct.setter
    def transaction_pct(self, transaction_pct):
        if 0.0 <= transaction_pct < 1.0:
            self._transaction_pct = transaction_pct
        else:
            raise ValueError('Transaction percentage needs to be between 0.0 and 1.0')

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, capital):
        self._capital = capital
        self._reset_history()

    def _get_observation(self):

        ohlcv = self._full_data.iloc[self.index].values
        capital = self.total_capital_history[-1]
        weight = self.weight_history[-1]

        return (ohlcv, capital, weight)

    def _reset_history(self):

        self.total_capital_history = [self.capital]
        self.capital_exposure_history = [0]
        self.weight_history = [0]
        self.returns_history = [0]
        self.tcosts_history = [0]