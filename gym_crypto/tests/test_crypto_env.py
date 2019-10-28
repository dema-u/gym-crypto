import gym
import unittest
import numpy as np

from gym_crypto.data_utils.data_utils import get_avaliable_currencies
from gym_crypto.configs import DEFAULT_CONFIG

class TestCryptoEnv(unittest.TestCase):

    def setUp(self):

        self.env = gym.make('gym-crypto-v0')
        self.env.configure_env(**DEFAULT_CONFIG)

    def test_initialized(self):
        currency = self.env.currency
        self.assertIsNotNone(currency)

    def test_reset(self):

        observation, info = self.env.reset()
        self.assertIsNotNone(observation)

    def test_step(self):

        self.test_reset()

        observation, reward, done, info = self.env.step(np.array(1))

        self.assertIsNotNone(observation)
        self.assertIsNotNone(reward)
        self.assertFalse(done)
        self.assertEqual(info, {})

    def test_completion(self):

        self.test_reset()
        iterations, done = 0, False

        while not done:
            iterations += 1
            observation, reward, done, info = self.env.step(np.array(1))

        self.assertTrue(done)

        return iterations

    def test_simulation_window(self):

        DEFAULT_CONFIG.update({'start_date':'2019-01-01', 'end_date':'2019-06-01'})
        self.env.configure_env(**DEFAULT_CONFIG)

        iterations = self.test_completion()

        self.assertIsNotNone(iterations)

    def test_render(self):

        iterations = self.test_completion()
        returns, weights = self.env.render()

        self.assertEqual(iterations, len(returns))
        self.assertEqual(iterations, len(weights))

    def test_config(self):
        self.assertEqual(DEFAULT_CONFIG['currency'], self.env.currency)
        self.assertEqual(DEFAULT_CONFIG['transaction_pct'], self.env.transaction_pct)
        self.assertEqual(DEFAULT_CONFIG['capital'], self.env.capital)
        self.assertEqual(DEFAULT_CONFIG['granularity'], self.env.granularity)

    def test_all_coins(self):

        all_currencies = get_avaliable_currencies()

        for currency in all_currencies:
            DEFAULT_CONFIG.update({'currency':currency})
            self.env.configure_env(**DEFAULT_CONFIG)
            self.assertIsNotNone(self.test_completion())

