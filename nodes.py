class Program:
    def __init__(self, body):
        self.body = body

class VariableDeclaration:
    def __init__(self, kind, declaration):
        self.kind = kind
        self.declaration = declaration

    def __repr__(self):
        return f"{self.kind} {self.declaration.id.name} = {self.declaration.init}"

class VariableDeclarator:
    def __init__(self, id, init):
        self.id = id
        self.init = init

    def __repr__(self):
        return f"{self.id.name} = {self.init}"

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"{self.left} {self.operator} {self.right}"

class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)
    
class GroupedExpression:
    def __init__(self, opening, expr, closing):
        self.opening = opening
        self.expr = expr
        self.closing = closing

    def __repr__(self):
        return f"{self.opening} {self.expr} {self.closing}"
    
class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        params = ", ".join(repr(s) for s in self.params)

        return f"prc {self.name}({params}) {self.body}"
    
class CallExpression:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        args = ", ".join(repr(s) for s in self.arguments)
        
        return f"{self.callee}({args})"
    
class BlockStatement:
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return "{ " + " ".join(repr(s) for s in self.body) + " }"
    
class ReturnStatement:
    def __init__(self, argument):
        self.argument = argument

    def __repr__(self):
        return f"return {self.argument}"
    
class ListExpression:
    def __init__(self, atoms):
        self.atoms = atoms

    def __repr__(self):
        return f"| {", ".join(repr(s) for s in self.atoms)} |"
    
class HashmapExpression:
    def __init__(self, values):
        self.values = values 
    
    def __repr__(self):
        return "{" + f", ".join([f"{key} : {value}" for key, value in self.values.items()]) + "}"