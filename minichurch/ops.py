import click
import sys

from minichurch.evaluator import syntax
from minichurch.evaluator.repl import LambdaREPL
from minichurch.lexer import lexer
from minichurch.parser import parser


# increase the recursion limit for big reductions
sys.setrecursionlimit(1000000)
def streamfile(file):
    """Takes a buffered reader and returns a generator that reads individual characters"""
    while True:
        chunk = file.read(1).decode("utf-8") 
        if not chunk:
            break
        yield chunk

@click.command()
@click.option('--file', '-f', default=None, type=click.File('rb'), help='Path to the file to parse')
@click.option('--explain', '-e', is_flag=True, help='Flag to explain each association step')
@click.option('--parsetree', '-p', is_flag=True, help='Flag to display the parse tree before the evaluation')
def run(file, explain, parsetree):
    """Simple lambda calculus executor, opens a repl shell if a file is not specified"""
    if file is not None:
        inputs = streamfile(file) # create a file stream for the lexer
        lexstream = lexer.lex(inputs) # 
        built_tree = parser.parse(lexstream)
        if parsetree:
            print(built_tree)
        output_val = parser.build(built_tree)
        showstep =  None
        if explain:
            showstep = syntax.create_showstep(output_val)
            print(f"Input:  {output_val.get()}")
        output_val = syntax.solver(output_val, showstep)
        if explain:
            print(f"\nResult: {output_val.get()}")
        else:
            print(output_val.get())
    else:
        prompt = LambdaREPL()
        prompt.prompt = '>>> '
        prompt.cmdloop('Starting minichurch Lambda Calculus REPL... \nUse "exit" or Ctrl-Z to quit, type "help" for more information')


if __name__ == '__main__':
    run()