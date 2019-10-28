## gym-crypto

OpenAI Gym compatible environment for crypto-currency trading.
The environment allows to change the currency the bot trades, the granularity of trading 
and starting capital of the agent. More configurability to come in the future. 

### Observation Space

The observation space is a tuple structured as follows:

```(OCHLV, Current Capital, Weight of the capital invested)```

OCHLV represents Open, Close, High, Low prices and Volume respectively. So the total capital invested into
a coin at any time is:

```(Current Capital)*(Weight of the capital invested)```

### Action Space

Action space is a single scalar between -1 and 1, which represents the percentage of the capital
that the agent has invested into the currency at the last time step.

-1 representing a full short position and 1 representing a full long position.

### Rewards

The reward is defined as the total amount of capital that has been gained/lost for that time-step.
This number includes the return on the investment as well as the transaction costs.

#### Usage

In order to train the agent, the enviroment first has to be configured. This example shows how to handle the
training and testing of the agents:

```python
import gym
from gym_crypto import configs

env = gym.make("gym-crypto-v0")
env.configure_env(**configs.DEFAULT_CONFIG)

### Train an agent on the environment

test_config = configs.DEFAULT_CONFIG.update({'start_date':'2019-01-01', 'end_date':'2019-06-01'})
env.configure_env(**test_config)

done = False
observation = env.reset()

while not done:
    action = agent.predict(observation)
    observation, _, done, _ = env.step(action)
    
returns, weights = env.render()
```

To get some results from the agent, a ```env.render()``` needs to be called, which will return
the capital returns as the first variable and weight allocation as the second variable. More detailed
results will be coming in the future.

#### Data

To futher inspect the data two methods can be called from the ```data_utils``` module.

```python
from gym_crypto.data_utils.data_utils import *

currencies = get_avaliable_currencies()
full_data = read_data('BTC')
```

All data was obtained from the Bitfinex API.
