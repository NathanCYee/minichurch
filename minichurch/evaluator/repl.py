from cmd import Cmd
import readline
from colorama import Fore

from minichurch.parser import parser
from minichurch.evaluator import syntax
from minichurch.lexer import lexer


class LambdaREPL(Cmd):
    def do_exec(self, statement):
        """exec [statement]
        Parse and evaluate a lambda calculus statement"""
        try:
            lexstream = lexer.lex(statement)
            built_tree = parser.parse(lexstream)
            output_val = parser.build(built_tree)
            print(f"\tInput:  \033[1m{output_val.get()}\033[0m")
            output_val = syntax.solver(output_val)
            print(f"\tResult: \033[1m{output_val.get()}\033[0m")
            readline.add_history(str(output_val.get()).replace('λ', '^'))
        except Exception as e:
            print(Fore.RED+str(e)+Fore.RESET)

    def do_explain(self, statement):
        """explain [statement]
        Parse and evaluate a lambda calculus statement while explaining each reduction step"""
        try:
            lexstream = lexer.lex(statement)
            built_tree = parser.parse(lexstream)
            output_val = parser.build(built_tree)
            showstep = syntax.create_showstep(output_val)
            print(f"\tInput:  \033[1m{output_val.get()}\033[0m")
            output_val = syntax.solver(output_val, showstep)
            print(f"\n\tResult: \033[1m{output_val.get()}\033[0m")
            readline.add_history(str(output_val.get()).replace('λ', '^'))
        except Exception as e:
            print(Fore.RED+str(e)+Fore.RESET)

    def do_show(self, statement):
        """show [statement]
        Parse a lambda calculus statement and display the syntax tree"""
        try:
            lexstream = lexer.lex(statement)
            built_tree = parser.parse(lexstream)
            print(built_tree)
        except Exception as e:
            print(Fore.RED+str(e)+Fore.RESET)
    
    def default(self, line: str) -> None:
        return self.do_exec(line)

    def do_exit(self, args):
        """Quit the REPL"""

        raise SystemExit