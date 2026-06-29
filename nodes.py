class Program:
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return f"{self.body}"

class VariableDeclaration:
    def __init__(self, declaration):
        self.declaration = declaration

    def __repr__(self):
        return f"var {self.declaration.id} = {self.declaration.init}"

class VariableAssignment:
    def __init__(self, operator, declaration):
        self.operator = operator
        self.declaration = declaration

    def __repr__(self):
        return f"set {self.declaration.id} {self.operator} {self.declaration.init}"

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
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f"[ {", ".join(repr(s) for s in self.values)} ]"
    
class HashmapExpression:
    def __init__(self, values):
        self.values = values 
    
    def __repr__(self):
        return "{" + f", ".join([f"{key} : {value}" for key, value in self.values.items()]) + "}"
    
class UnaryExpression:
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value 
    
    def __repr__(self):
        return f"{self.operator}{self.value}"
    
class PostfixExpression:
    def __init__(self, exp, start_exp, end_exp=None):
        self.exp = exp
        self.start_exp = start_exp
        self.end_exp = end_exp

    def __repr__(self):
        return f"{self.exp}[{self.start_exp}{f":{self.end_exp}" if self.end_exp is not None else ""}]"
    
class IfStatement:
    def __init__(self, condition, body, alternate):
        self.condition = condition
        self.body = body
        self.alternate = alternate

    def __repr__(self):
        return "IF TEST"

class LoopStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return "LOOP TEST"

class ContinueStatement:
    def __init__(self):
        pass

    def __repr__(self):
        return "continue"

class BreakStatement:
    def __init__(self):
        pass

    def __repr__(self):
        return "break"

class FunctionExpression:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        params = ", ".join(repr(s) for s in self.params)

        return f"prc ({params}) {self.body}"
