from setuptools import setup
setup(
  name = 'tictactoe_learn',
  packages = ['tictactoe_learn'], # this must be the same as the name above
  version = '0.0.1',
  description = 'A learning program that plays with the users and depends on their inputs to learn optimal strategy in the classic game of tic-tac-toe.',
  author = 'Avikalp Srivastava',
  author_email = 'avikalp22@iitkgp.ac.in',
  url = 'https://github.com/Avikalp7/TicTacToe-Reinforcement-Learning', 
  keywords = ['IIT', 'KGP', 'Tic Tac Toe', 'Tic Tac', 'Avikalp Srivastava', 'CG Accumulator', 'Python', 'Reinforcement Learning', 'Machine Learning'], 
  
  license = 'MIT',
  
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=['prettytable'],
)
