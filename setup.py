from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gym-crypto',
      packages=['gym_crypto'],
      version='0.0.2',
      licence='MIT',
      description='Reinforcement Learning OpenAI Gym environment for crypto-currency trading.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Dema Ushchapovskyy, Suraj Tirupati',
      author_email='du116@ic.ac.uk',
      download_url='https://github.com/dema-u/gym-crypto/archive/0.0.1.tar.gz',
      keywords=['RL', 'OpenAI', 'Gym'],
      install_requires=['gym', 'pandas', 'numpy']
)