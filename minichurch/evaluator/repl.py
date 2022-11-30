from cmd import Cmd
import readline
from colorama import Fore

from minichurch.parser import parser
from minichurch.evaluator import syntax
from minichurch.lexer import lexer


def create_tree(statement):
    # create an input stream
    lexstream = lexer.lex(statement)
    # parse the stream into a parse tree
    built_tree = parser.parse(lexstream)
    return built_tree


def push_output(syntax_statement):
    """Push a compiled statement onto the output"""
    # replace lambdas with chevrons and strip spaces
    res = str(syntax_statement.get()).replace('λ', '^').replace(' ', '')
    # push onto history to be accessed using up key
    readline.add_history(res)


class LambdaREPL(Cmd):
    def do_exec(self, statement):
        """exec [statement]
        Parse and evaluate a lambda calculus statement"""
        try:
            built_tree = create_tree(statement)
            # take the parse tree and build a compiled instruction
            output_val = parser.build(built_tree)
            print(f"\tInput:  \033[1m{output_val.get()}\033[0m")
            # interpret and solve the instruction
            output_val = syntax.solver(output_val)
            # rebind variables that are conflicting
            syntax.renamer(output_val)
            print(f"\tResult: \033[1m{output_val.get()}\033[0m")
            # add the evaluated result to history
            push_output(output_val)

        except Exception as e:
            # display error in red
            print(Fore.RED+str(e)+Fore.RESET)

    def do_explain(self, statement):
        """explain [statement]
        Parse and evaluate a lambda calculus statement while explaining each reduction step"""
        try:
            built_tree = create_tree(statement)
            # take the parse tree and build a compiled instruction
            output_val = parser.build(built_tree)
            # create a display function that will count steps and display the result
            showstep = syntax.create_showstep(output_val)
            print(f"\tInput:  \033[1m{output_val.get()}\033[0m")
            # interpret and solve the instruction
            output_val = syntax.solver(output_val, showstep)
            # rebind variables that are conflicting
            syntax.renamer(output_val, showstep=showstep)
            print(f"\n\tResult: \033[1m{output_val.get()}\033[0m")
            # add the evaluated result to history
            push_output(output_val)
        except Exception as e:
            # display error in red
            print(Fore.RED+str(e)+Fore.RESET)

    def do_show(self, statement):
        """show [statement]
        Parse a lambda calculus statement and display the syntax tree"""
        try:
            built_tree = create_tree(statement)
            print(built_tree)
        except Exception as e:
            # display error in red
            print(Fore.RED+str(e)+Fore.RESET)

    def default(self, line: str) -> None:
        return self.do_exec(line)

    def do_exit(self, args):
        """Quit the REPL"""

        raise SystemExit
