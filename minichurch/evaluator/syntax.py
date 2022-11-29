import copy
from colorama import Fore

class Expression:
    def bind(self, expr, showstep=None) -> bool:
        """Associates a new value to the object"""
        return False

    def get(self):
        """returns the bounded/evaluated values or itself"""
        return self

    def get_inner(self):
        """retrieve the innermost Application"""
        return self.get()

    def __repr__(self):
        return str(self)


class Name(Expression):
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.value = None

    def bind(self, expr, showstep=None):
        # bind value if not bound yet
        if self.value is None:
            self.value = expr
            if showstep is not None:
                print(f"{Fore.GREEN+str(self.symbol)+Fore.RESET} becomes {Fore.GREEN+str(self.value)+Fore.RESET}")
            return True
        else:
            # pass through if already bound
            return self.get().bind(expr)

    def get(self):
        # retrieve self if floor, else pass through a copy
        return self if self.value is None else copy.deepcopy(self.value.get())
    
    def get_inner(self):
        return self.get()

    def __str__(self):
        # print string value of name if not bound
        if self.value is None:
            if self.symbol is not None:
                return self.symbol
            else:
                return str(id(self))
        else:
            # pass through to value
            return str(self.value.get())


class Function(Expression):
    def __init__(self, name=None):
        self.name = name
        self.inner_data = None
        self.bound = False

    def set_expr(self, expr):
        self.inner_data = expr
        return self

    def bind(self, expr, showstep=None):
        if self.bound:
            # pass through to inner since the function is already evaluated
            return self.inner_data.bind(expr.get())
        else:
            self.name.bind(expr.get(), showstep)
            self.inner_data = self.inner_data.get()
            self.bound = True  # mark as variable bound
            return True

    def get(self):
        self.inner_data = self.inner_data.get()
        return self.inner_data if self.bound else self

    def get_inner(self):
        return self.inner_data.get_inner()

    def __str__(self):
        if self.bound:
            return str(self.inner_data.get())
        else:
            return f"λ {self.name.get()}. {self.inner_data.get()}"


class Application(Expression):
    def __init__(self):
        self.left = None
        self.right = None
        self.applied = False

    def inner(self):
        return self.left.get()

    def set_left(self, expr):
        self.left = expr
        return self

    def set_right(self, expr):
        self.right = expr
        return self

    def bind(self, expr, showstep=None):
        # simplify
        self.right = self.right.get()
        self.left = self.left.get()
        if self.right is None:
            return False
        if isinstance(self.left, Application):
            # reduce the left side until you can pass in values
            while isinstance(self.left, Application):
                bound = self.left.bind(None, showstep)  # bind inner
                self.left = self.left.get()  # retrieve result
                if not bound: # reduced down to a name
                    return False
            if showstep is not None:
                print(f"\nBind {Fore.GREEN+str(self.right)+Fore.RESET} to {Fore.GREEN+str(self.left)+Fore.RESET}")
            self.left.bind(self.right, showstep)  # bind outer
            self.left = self.left.get()  # retrieve result
            self.applied = True
            if showstep is not None:
                showstep()
            return True
        if isinstance(self.left, Function):  # only bind functions
            if showstep is not None:
                print(f"\nBind {Fore.GREEN+str(self.right)+Fore.RESET} to {Fore.GREEN+str(self.left)+Fore.RESET}")
            self.left.bind(self.right, showstep)
            self.left = self.left.get()
            self.applied = True
            if showstep is not None:
                showstep()
            return True
        return False

    def get(self):
        return self.left if self.applied else self
    
    def get_inner(self):
        return self

    def __str__(self):
        if self.right is not None and not self.applied:
            return f"({self.left.get()} {self.right.get()})"
        else:
            return str(self.left.get())

def create_showstep(expression: Expression) -> Function:
    """Create a function that will count steps and display the full expression"""
    count = 1
    def showstep():
        nonlocal count
        print(str(count)+'. '+Fore.BLUE+str(expression.get())+Fore.RESET)
        count += 1
    return showstep

def solver(expression: Expression, showstep=None) -> Expression:
    """Given an expression, reduce it until it is no longer possible"""
    # bind every application until it is reduced as much as possible
    while isinstance(expression, Application):
        evaled = expression.bind(None, showstep)
        expression = expression.get()
        if not evaled: # binding did not work, left is expression or name
            break
    # retrieve the body of the expression
    innerexpr = expression.get_inner()
    if isinstance(innerexpr, Application):
        # left was fully evaluated, evaluate right
        if innerexpr == expression:
            solver(expression.right, showstep)
        else:
            # reduce the body of a function
            solver(innerexpr, showstep)
    return expression.get()