import typing
from minichurch.lexer.tokens import *

def lex(inputstream: typing.Generator[str, None, None])-> typing.Generator[Token, None, None]:
    """recieve an input generator and become a functional generator that lazily evaluates tokens"""
    scope = 0

    def add_block():
        nonlocal scope
        """Increments the current scope and creates a new opening block"""
        scope += 1
        new_block = OpeningBlock(scope)
        return new_block

    def remove_block():
        nonlocal scope
        """Creates a new opening block and decrements the current scope"""
        new_block = ClosingBlock(scope)
        scope -= 1
        return new_block
    
    def get_func():
        """retrieve the static token value"""
        return func_val
    
    def get_body():
        """retrieve the static body val"""
        return body_val

    lookup_table = {'^': get_func,'λ': get_func, '.': get_body,
                    '(': add_block, ')': remove_block}

    for char in inputstream:
        if char.isspace():
            # advance past whitespace
            continue
        # known symbol separator, return its object
        if char in lookup_table:
            yield lookup_table[char]()
        # yield a name because the character is not known
        else:
            yield Name(char)