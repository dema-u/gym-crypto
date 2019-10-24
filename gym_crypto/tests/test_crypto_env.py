import gym
import unittest
import numpy as np

class TestCryptoEnv(unittest.TestCase):

    def setUp(self):

        self.env = gym.make('gym-crypto-v0')

        start_date = '2018-01-01'
        end_date = '2019-01-01'

        currency = 'BTC'
        granularity = '15min'
        transaction_pct = 0.001
        capital = 100

        kwargs = {'currency':currency, 'granularity':granularity,
                  'transaction_pct':transaction_pct, 'capital':capital,
                  'start_date': start_date, 'end_date':end_date}

        self.env.configure_env(**kwargs)

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

        self.env.set_simulation_window('2018-01-01', '2019-01-01')
        iterations = self.test_completion()

        self.assertEqual(iterations, 17519)

    def test_render(self):

        iterations = self.test_completion()
        returns, weights = self.env.render()

        self.assertEqual(iterations, len(returns))
        self.assertEqual(iterations, len(weights))
