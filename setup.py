from setuptools import setup

tests_require = [
    'pytest'
]

setup(
    name='minichurch',
    version='0.0.1',
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
