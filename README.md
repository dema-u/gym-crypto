## gym-crypto

OpenAI Gym compatible environment for crypto-currency trading.
The environment allows to change the currency the bot trades, the granularity of trading 
and starting capital of the agent. More configurability to come in the future. 

### Observation Space

The observation space is a tuple structured as follows:

```(OCHLV, Current Capital, Weight of the capital invested)```

OCHLV represents Open, Close, High, Low prices and Volume respectively.

### Action Space

Action space is a single scalar between -1 and 1, which represents the percentage of the capital
that the agent has invested into the currency at the last time step.

-1 representing a full short position and 1 representing a full long position.

### Rewards

The reward is defined as the total amount of capital that has been gained/lost for that time-step.
This number includes the return on the investment as well as the transaction costs.

#### Usage

In order to train the agent, the enviroment first has to be configured. This can be done as follows:

```python
import gym

env = gym.make("gym-crypto-v0")

start_date = '2018-01-01'
end_date = '2019-01-01'

currency = 'BTC'
granularity = '15min'
transaction_pct = 0.001
capital = 100

kwargs = {'currency':currency, 'granularity':granularity,
          'transaction_pct':transaction_pct, 'capital':capital,
          'start_date': start_date, 'end_date':end_date}
          
env.configure_env(**kwargs)
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
