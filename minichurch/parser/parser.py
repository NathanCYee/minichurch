import typing

from minichurch.evaluator import syntax
from minichurch.lexer import tokens
from minichurch.parser import parsertypes


def create_innerstream(layer: int, lexstream: typing.Generator[tokens.Token, None, None]) -> typing.Generator[tokens.Token, None, None]:
    """Takes a layer number and a stream and returns a generator that will yield until it sees a closing block with the matching layer number"""
    for token in lexstream:
        yield token
        if isinstance(token, tokens.ClosingBlock) and token.value == layer:
            break


def parse(lexstream: typing.Generator[tokens.Token, None, None]) -> parsertypes.SyntaxTree:
    """Take a generator of tokens and parse them into a syntax tree"""
    # <expression> := <name>|<function>|<application>
    buffer = []
    for token in lexstream:
        # retrieve the next values to parse a function
        if isinstance(token, tokens.Function):
            # <function> := λ <name> . <expression>
            tempvar = parsertypes.FunctionTree()  # create a function to add to block
            nameval = next(lexstream)  # retrieve the name of the function
            # make sure a name follows the function definition
            if not isinstance(nameval, tokens.Name):
                raise TypeError(
                    "Expected named value after function declaration")
            # check to make sure body separator is in place
            if not isinstance(next(lexstream), tokens.Body):
                raise TypeError("Expected body value after name separator")
            tempvar.left = nameval
            # parse the body as the right of the tree
            tempvar.right = parse(lexstream)  # parse the rest as a body
            # add tempvar to buffer for association processing
            buffer.append(tempvar)
            continue
        # create a new stream and parse it as a block, then append to the buffer
        if isinstance(token, tokens.OpeningBlock):
            # only grab values from inside the block
            # parse until the end of the block is reached
            innerstream = create_innerstream(token.value, lexstream)
            buffer.append(parse(innerstream))  # spawn a new processing step
            continue
        # end of the readable stream, end the parsing and begin evaluation
        if isinstance(token, tokens.ClosingBlock):
            break  # break and consolidate to return
        else:
            # encountered a name
            buffer.append(token)
    # nothing encountered, this block is empty
    if len(buffer) == 0:
        return None
    # create a new syntax tree to output
    output_val = parsertypes.SyntaxTree()
    # pop from the buffer and associate the left(so far parsed) to the right (newly encountered)
    # makes the function left associative, binds right to left
    while len(buffer) != 0:
        # start binding to the left
        if output_val.left is None:
            output_val.left = buffer.pop(0)
        else:
            # create a new tree that binds the current tree (left) to a new value on the right
            new_val = parsertypes.SyntaxTree()
            # current right is none, bind the singular current value with the new
            if output_val.right is None:
                new_val.left = output_val.left
            else:
                # current tree is populated, create a new empty tree to bind to the old
                new_val.left = output_val
            # set the binding value to be the latest value
            new_val.right = buffer.pop(0)
            # updated tree is now head
            output_val = new_val
    # find the most populated tree to return
    if output_val.right is None:
        return output_val.left
    return output_val


def build(body: typing.Union[parsertypes.SyntaxTree, tokens.Name], outerscope: parsertypes.Scope = None) -> syntax.Expression:
    """Takes a syntax tree or name and scope block and returns an evaluatable syntax expression"""
    # base scope
    if outerscope is None:
        outerscope = parsertypes.Scope()
    # <expression> := <name>|<function>|<application>
    # create or bind a new name
    if isinstance(body, tokens.Name):
        if not outerscope.name_exists(body.value):
            outerscope.add_name(body.value)
        return outerscope.find_name(body.value)
    if isinstance(body, parsertypes.FunctionTree):
        # create a function with the current scope
        return create_function(body, outerscope)
    else:
        # create an application with the current scope
        return create_application(body, outerscope)


def create_application(body: parsertypes.SyntaxTree, outerscope: parsertypes.Scope) -> syntax.Application:
    """Creates a syntax application that applies the right value to the left value"""
    scope = parsertypes.Scope(outer=outerscope)  # create a new scope for binding
    # <application> := <expression> <expression>
    return syntax.Application().set_left(
        build(body.left, scope)  # recursively build the left side
    ).set_right(
        build(body.right, scope)  # recursively build the right side
    )


def create_function(body: parsertypes.FunctionTree, outerscope: parsertypes.Scope) -> syntax.Function:
    """creates a syntax function with a name and body binding"""
    funcscope = parsertypes.Scope(outer=outerscope)  # create a new scope for the function
    # <function> := λ <name> . <expression>
    name = body.left  # retrieve the name
    funcscope.add_name(name.value)  # bind the name to the scope
    # create a new function object with the binded name
    newfunc = syntax.Function(funcscope.find_name(
        name.value)
    )
    # recursively build the expression body of the function
    newfunc.set_expr(
        build(body.right, funcscope)
    )
    return newfunc
