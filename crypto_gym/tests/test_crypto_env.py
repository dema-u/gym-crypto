import gym
import unittest
import numpy as np

class TestCryptoEnv(unittest.TestCase):

    def setUp(self):

        self.env = gym.make('crypto-gym-v0')

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
        i = 0
        done = False

        while not done:
            i += 1
            observation, reward, done, info = self.env.step(np.array(1))

        self.assertTrue(done)

        return i

    def test_simulation_window(self):

        self.env.set_simulation_window(5, 10)
        iterations = self.test_completion()

        self.assertEqual(iterations, 4)

    def test_reconfigure_currency(self):

        self.env.configure_currency('ETH')

    def test_render(self):

        iterations = self.test_completion()
        returns, weights = self.env.render()

        self.assertEqual(iterations, len(returns))
        self.assertEqual(iterations, len(weights))
