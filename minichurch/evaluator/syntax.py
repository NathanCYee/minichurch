import copy
import string
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

    def replicate(self, replacement=None):
        """create a copy of the given expression while not replacing bound Names"""
        pass

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
                print(
                    f"{Fore.GREEN+str(self.symbol)+Fore.RESET} becomes {Fore.GREEN+str(self.value)+Fore.RESET}")
            return True
        else:
            # pass through if already bound
            return self.get().bind(expr)

    def get(self):
        # retrieve self if floor, else pass through a copy
        return self if self.value is None else self.value.get().replicate()

    def get_inner(self):
        return self.get()

    def replicate(self, replacement=None):
        if replacement is None:
            replacement = {}
        # unbounded name
        if self.value is None:
            # name has been marked for copy
            if self in replacement:
                # retrieve replacement
                return replacement[self]
            else:
                # return self (no copy)
                return self
        else:
            # pass through
            return self.value.get().replicate(replacement)

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
        return self.inner_data.get() if self.bound else self

    def get_inner(self):
        return self.inner_data.get_inner()

    def replicate(self, replacement=None):
        if replacement is None:
            replacement = {}
        # pass through
        if self.bound:
            return self.inner_data.get().replicate(replacement)
        else:
            # create a new name to copy
            newname = copy.deepcopy(self.name)
            # create a copy of the replacements
            # instead of mutating the commonly passed one
            rep = replacement.copy()
            # bind the new replacement
            rep[self.name] = newname
            # replicate the expr of the function
            newinner = self.inner_data.replicate(rep)
            return Function(newname).set_expr(newinner)

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
                if not bound:  # reduced down to a name
                    return False
            
        if isinstance(self.left, Function):  # only bind functions
            if showstep is not None:
                print(
                    f"\nAssociate {Fore.GREEN+str(self.right)+Fore.RESET} with {Fore.GREEN+str(self.left)+Fore.RESET}")
            self.left.bind(self.right, showstep) # bind outer
            self.left = self.left.get()# retrieve result
            self.applied = True
            if showstep is not None:
                showstep()
            return True
        # right side becomes left-most outer-most redex
        elif isinstance(self.right, Expression):
            self.right.bind(None, showstep) # bind right outermost
            self.right = self.right.get()
        return False

    def get(self):
        return self.left.get() if self.applied else self

    def get_inner(self):
        return self

    def replicate(self, replacement=None):
        if replacement is None:
            replacement = {}
        # pass through
        if self.applied:
            return self.left.get().replicate(replacement)
        else:
            # create a new application with copies
            return Application().set_left(self.left.get().replicate(replacement)).set_right(self.right.get().replicate(replacement))

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
        if not evaled:  # binding did not work, left is expression or name
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


valid_alphabet = list(string.ascii_lowercase)
valid_alphabet.extend(list(string.ascii_uppercase))


def get_next_name(cur_names: dict):
    """Get a single-character alphabetical new name string that is not in cur_names"""
    for char in valid_alphabet:
        if char not in cur_names:
            return char
    raise Exception("Could not find any more alphabetical names")


def renamer(expression: Expression, cur_names: dict = None, showstep = None):
    """Loops through a statement and renames Names that have the same name in the same scope"""
    # set cur_names to empty if none (create new empty)
    if cur_names is None:
        cur_names = {}
    expr = expression.get()
    if isinstance(expr, Name):
        if expr.symbol in cur_names:
            if expr != cur_names[expr.symbol]:
                try:
                    # get new name
                    new_symbol = get_next_name(cur_names)
                    old_symbol = expr.symbol
                    # change symbol
                    expr.symbol = new_symbol
                    # display message
                    if showstep is not None:
                        print(
                            f"\nRenaming {Fore.GREEN+old_symbol+Fore.RESET} to {Fore.GREEN+new_symbol+Fore.RESET}")
                        showstep()
                    cur_names[new_symbol] = expr
                except:
                    if showstep is not None:
                        print("Could not rename further...")
                return
            else:  # ignore, already seen
                return
        else:  # register new symbol
            cur_names[expr.symbol] = expr
    elif isinstance(expr, Application):
        # rename for left and right sides, copy current dict to prevent mutation
        renamer(expr.left.get(), cur_names.copy(), showstep)
        renamer(expr.right.get(), cur_names.copy(), showstep)
    elif isinstance(expr, Function):
        # register new name on right or rename it
        renamer(expr.name.get(), cur_names, showstep)
        # use updated dict to update inner
        renamer(expr.inner_data.get(), cur_names.copy(), showstep)
