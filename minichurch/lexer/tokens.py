class Token:
    """Base class for a lexer token"""
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self)


class OpeningBlock(Token):
    """Token to represent an opening parentheses to parse.
    Holds the scope number under value to deliminate the depth"""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'{self.value}('

class ClosingBlock(Token):
    """Token to represent a closing parentheses to parse.
    Holds the scope number under value to deliminate the depth"""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'{self.value})'

class Name(Token):
    """Token to represent a Name instance
    Holds the string value of the encountered value"""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)


class Function(Token):
    """Token to represent the starting character of a Function expression"""
    def __init__(self, value):
        self.value = '^'
    
    def __str__(self):
        return 'λ'


class Body(Token):
    """Token to represent the name/body separator of a function expression"""
    def __init__(self, value):
        self.value = '.'
    def __str__(self):
        return '.'


func_val = Function(None)
body_val = Body(None)
