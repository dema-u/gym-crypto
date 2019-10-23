from setuptools import setup

setup(name='crypto-gym',
      packages=['crypto_gym'],
      version='0.0.2',
      licence='MIT',
      description='Reinforcement Learning OpenAI Gym environment for crypto-currency trading.',
      author='Dema Ushchapovskyy, Suraj Tirupati',
      author_email='du116@ic.ac.uk',
      download_url='https://github.com/dema-u/crypto-gym/archive/0.0.1.tar.gz',
      keywords=['RL', 'OpenAI', 'Gym'],
      install_requires=['gym', 'pandas', 'numpy']
)