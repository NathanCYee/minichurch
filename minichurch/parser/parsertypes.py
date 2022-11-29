
from minichurch.evaluator import syntax

class Scope:
    """A scope block that emulates a runtime stack block with a pointer to the parent stack"""
    def __init__(self, outer=None):
        self._lookuptable = {}
        self._outerblock = outer

    def find_name(self, name: str) -> syntax.Name:
        """Find a syntax Name object that matches the given name in the scope"""
        if name in self._lookuptable:
            # in current scope, return the localmost value
            return self._lookuptable[name]
        elif self._outerblock is not None:
            # search recursively outside the scope
            return self._outerblock.find_name(name)
        else:
            # name not found at base level scope
            raise NameError("Could not find name binding")

    def name_exists(self, name: str) -> bool:
        """Check if the name has been bound and available in scope"""
        if name in self._lookuptable:
            # in current scope
            return True
        elif self._outerblock is not None:
            # check outer scope
            return self._outerblock.name_exists(name)
        return False # not found anywhere

    def add_name(self, name: str):
        """Bind a new name to the current scope"""
        # name already bound, could not bind new name
        if name in self._lookuptable:
            return False
        else:
            # add a new name to the lookup table
            self._lookuptable[name] = syntax.Name(name)
            return True


class SyntaxTree:
    """Binary tree that represents an application of right to left"""
    def __init__(self):
        self.left = None
        self.right = None

    def __str__(self):
        return f"APPLICATION(\n{''.join(['    '+i for i in str(self.left).splitlines(True)])}, \n{''.join(['    '+i for i in str(self.right).splitlines(True)])}\n)"

    def __repr__(self):
        return str(self)


class FunctionTree(SyntaxTree):
    """Binary tree with left being a name object and right being the body of the function"""
    def __init__(self):
        self.left = None
        self.right = None

    def __str__(self):
        return f"FUNCTION(\n{''.join(['    '+i for i in str(self.left).splitlines(True)])}, \n{''.join(['    '+i for i in str(self.right).splitlines(True)])}\n)"

    def __repr__(self):
        return str(self)
