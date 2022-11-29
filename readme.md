# minichurch

A simple python lambda calculus interpreter. Includes file parsing and REPL.
Executor accepts both the lambda character "λ" and the chevron character "^" for function definitions

## Table of Contents

- [Features](https://github.com/NathanCYee/minichurch#Features)
- [Setup and Install](https://github.com/NathanCYee/minichurch#Setup-and-Install)
- [Usage](https://github.com/NathanCYee/minichurch#Usage)
- [Technologies](https://github.com/NathanCYee/minichurch#Technologies)
- [License](https://github.com/NathanCYee/minichurch#License)

## Features

- TBD

## Setup and Install

Please make sure python 3 is installed (working on python 3.8).

- Download the library by cloning it using `git clone https://github.com/NathanCYee/minichurch.git`
- Navigate to the folder in which the project is stored (e.g. `cd minichurch`)
- Install the package using `python setup.py install`
- Run the application using the command `minichurch`

## Usage

```
Usage: minichurch [OPTIONS]

  Simple lambda calculus executor, opens a repl shell if a file is not
  specified

Options:
  -f, --file FILENAME  Path to the file to parse
  -e, --explain        Flag to explain each association step
  -p, --parsetree      Flag to display the parse tree before the evaluation
  --help               Show this message and exit.
```

Calling the minichurch command without any arguments will open a repl window.
### REPL Commands
- `exec [statement]` - executes a lambda calculus statement and displays the result (default behavior without any command)
- `explain [statement]` - executes a lambda calculus statement and displays the result along with every binding step
- `show [statement]` - parses a lambda calculus statement and displays the resulting parse tree
- `help` - displays the help menu
- `exit` - quits the REPL (can also be done with Ctrl-Z)

## Technologies

Project was built with:

- Python 3
    - [click](https://click.palletsprojects.com/en/8.1.x/) - easy CLI tool framework
    - [cmd](https://docs.python.org/3/library/cmd.html) - built-in repl tool maker
    - [colorama](https://pypi.org/project/colorama/) - text coloring library

# License
BSD 3-Clause