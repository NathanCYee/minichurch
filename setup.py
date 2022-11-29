from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='minichurch',
    version='0.0.1',
    description='A simple python lambda calculus interpreter. Includes file parsing and REPL.',
    url='https://github.com/NathanCYee/minichurch',
    author='Nathan Yee',
    license='BSD 3-Clause',
    install_requires=[
        'click',
        'colorama'
    ],
    packages=['minichurch','minichurch.evaluator','minichurch.lexer','minichurch.parser'],
    # tests_require=tests_require,
    extras_require={
        'test': tests_require
    },
    entry_points={
        'console_scripts': ['minichurch=minichurch.ops:run']
    }
)
