import helper
from tokens.keywords import Keywords
from tokens.punctions import Punctions
from tokens.operators import Operators


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

class Parser:
    def __init__(self):
        self.index = 0
        self.tokens = []

    def match(self, expected, match_type):
        c_token = self.peek()

        if (c_token[match_type] == expected):
            self.index += 1

            return c_token
        
        raise TypeError(f"Expected token {expected}, but got {c_token["value"]}")

    def peek(self):        
        return self.tokens[self.index]

    def parse_program(self, tokens):
        self.tokens = tokens
        self.body = []

        while (not helper.is_eof(self.index, self.tokens)):
            stmt = self.parse_statement()

            self.body.append(stmt)

        return Program(body=self.body)

    def parse_statement(self):
        current_token = self.peek()

        if (current_token["value"] == Keywords.VAR):
            return self.parse_var()
        elif (current_token["value"] == Keywords.SET):
            return self.parse_set()
        elif (current_token["value"] == Keywords.PRC):
            return self.parse_function()
        elif (current_token["value"] == Keywords.RETURN):
            return self.parse_return()
        elif (current_token["type"] == "IDENTIFIER" or current_token["type"] == "NUMBER"):
            return self.parse_expression()

        raise TypeError(f"Unknown statement starting with {self.peek()["value"]}")

    def parse_var(self):
        self.match(Keywords.VAR, "value")
        identifier = self.match("IDENTIFIER", "type")
        self.match(Operators.EQUAL, "value")
        expression = self.parse_expression()

        return VariableDeclaration(kind="var", declaration=VariableDeclarator(id=Identifier(name=identifier["value"]), init=expression))
    
    def parse_set(self):
        self.match(Keywords.SET, "value")
        identifier = self.match("IDENTIFIER", "type")
        self.match(Operators.EQUAL, "value")
        expression = self.parse_expression()

        return VariableDeclaration(kind="set", declaration=VariableDeclarator(id=Identifier(name=identifier["value"]), init=expression))

    def parse_expression(self):
        left = self.parse_term()

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["type"] == "OPERATOR"):
            operator = self.match("OPERATOR", "type")["value"]
            right = self.parse_term()

            left = BinaryExpression(left=left, operator=operator, right=right)

        return left
 
    def parse_term(self):
        current = self.peek()
        
        if (current["type"] == "NUMBER"):
            self.match("NUMBER", "type")

            return Literal(current["value"])
        elif (current["type"] == "IDENTIFIER"):
            self.match("IDENTIFIER", "type")
            next_peek = self.peek()

            if (next_peek["value"] == "("):
                self.match(Punctions.PARANTHESSES_O, "value")
                args = self.parse_args()
                self.match(Punctions.PARANTHESSES_C, "value")

                return CallExpression(Identifier(current["value"]), args)
            else:
                return Identifier(current["value"])
        elif (current["value"] == "("):
            self.match(Punctions.PARANTHESSES_O, "value")
            expr = self.parse_expression()
            self.match(Punctions.PARANTHESSES_C, "value")

            return GroupedExpression(Punctions.PARANTHESSES_O, expr, Punctions.PARANTHESSES_C)
        elif (current["type"] == "STRING"):
            self.match("STRING", "type")

            return Literal(current["value"])
        
        raise TypeError(f"Expected term, but got {current["value"]}")
    
    def parse_function(self):
        self.match(Keywords.PRC, "value")
        identifier = self.match("IDENTIFIER", "type")
        self.match(Punctions.PARANTHESSES_O, "value")
        params = self.parse_params()
        self.match(Punctions.PARANTHESSES_C, "value")
        self.match(Punctions.CURVED_O, "value")
        body = self.parse_block()
        self.match(Punctions.CURVED_C, "value")

        return FunctionDeclaration(Identifier(identifier["value"]), params, body)
    
    def parse_block(self):
        body = []

        while (self.peek()["value"] != Punctions.CURVED_C):
            statement = self.parse_statement()

            body.append(statement)

        return BlockStatement(body)
    
    def parse_params(self):
        params = []

        while (self.peek()["type"] == "IDENTIFIER"):
            param = self.match("IDENTIFIER", "type")["value"]

            params.append(Identifier(param))

        return params
    
    def parse_args(self):
        params = []

        while (self.peek()["type"] in ("NUMBER", "STRING")):
            # TODO: multiple param type
            param = self.match("NUMBER", "type")["value"]

            params.append(Literal(param))

        return params
    
    def parse_return(self):
        self.match(Keywords.RETURN, "value")
        expr = self.parse_expression()

        return ReturnStatement(expr)


def main():
    parser = Parser()

    sample = [
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "NUMBER", "value": "42"},
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "y"},
        {"type": "OPERATOR", "value": "="},
        {"type": "NUMBER", "value": "99"},
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "z"},
        {"type": "OPERATOR", "value": "="},
        {"type": "IDENTIFIER", "value": "x"},
        {"type": "OPERATOR", "value": "+"},
        {"type": "PUNCTION", "value": "("},
        {"type": "IDENTIFIER", "value": "y"},
        {"type": "OPERATOR", "value": "+"},
        {"type": "NUMBER", "value": "3"},
        {"type": "PUNCTION", "value": ")"},
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "_g"},
        {"type": "OPERATOR", "value": "="},
        {"type": "STRING", "value": "ABC"},
        {"type": "KEYWORDS", "value": "set"},
        {"type": "IDENTIFIER", "value": "x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "NUMBER", "value": "32"},
        {"type": "OPERATOR", "value": "%"},
        {"type": "NUMBER", "value": "2"},
        {"type": "KEYWORDS", "value": "set"},
        {"type": "IDENTIFIER", "value": "x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "IDENTIFIER", "value": "y"},
        {"type": "OPERATOR", "value": "*"},
        {"type": "IDENTIFIER", "value": "z"},
        {"type": "OPERATOR", "value": "+"},
        {"type": "NUMBER", "value": "22"},
        {"type": "KEYWORDS", "value": "prc"},
        {"type": "IDENTIFIER", "value": "foo"},
        {"type": "PUNCTION", "value": "("},
        {"type": "IDENTIFIER", "value": "param_1"},
        {"type": "IDENTIFIER", "value": "param_2"},
        {"type": "PUNCTION", "value": ")"},
        {"type": "PUNCTION", "value": "{"},
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "new_x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "NUMBER", "value": "12"},
        {"type": "KEYWORDS", "value": "set"},
        {"type": "IDENTIFIER", "value": "new_x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "NUMBER", "value": "99"},
        {"type": "KEYWORDS", "value": "set"},
        {"type": "IDENTIFIER", "value": "new_x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "PUNCTION", "value": "("},
        {"type": "IDENTIFIER", "value": "new_x"},
        {"type": "OPERATOR", "value": "+"},
        {"type": "NUMBER", "value": "2"},
        {"type": "PUNCTION", "value": ")"},
        {"type": "OPERATOR", "value": "*"},
        {"type": "NUMBER", "value": "99"},
        {"type": "PUNCTION", "value": "}"},
        {"type": "IDENTIFIER", "value": "foo"},
        {"type": "PUNCTION", "value": "("},
        {"type": "PUNCTION", "value": ")"},
    ]


    for token in parser.parse_program(sample).body:
        print(repr(token))


if __name__ == "__main__":
    main()
