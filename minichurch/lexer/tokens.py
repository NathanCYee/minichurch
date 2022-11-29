class Token:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self)


class OpeningBlock(Token):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'{self.value}('

class ClosingBlock(Token):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f'{self.value})'

class Name(Token):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)


class Function(Token):
    def __init__(self, value):
        self.value = '^'
    
    def __str__(self):
        return 'λ'


class Body(Token):
    def __init__(self, value):
        self.value = '.'
    def __str__(self):
        return '.'


func_val = Function(None)
body_val = Body(None)
