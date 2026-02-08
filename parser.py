import helper
import nodes
from tokens.keywords import Keywords
from tokens.punctuations import Punctuations
from tokens.operators import Operators


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

    def match_assignment(self):
        c_token = self.peek()

        if (c_token["value"] in (Operators.EQUAL, Operators.A_EQUAL, Operators.M_EQUAL, Operators.S_EQUAL, Operators.D_EQUAL, Operators.P_EQUAL, Operators.MO_EQUAL)):
            self.index += 1

            return c_token
        else:
            raise TypeError(f"Expected token assignment, but got {c_token["value"]}")

    def peek(self):        
        return self.tokens[self.index]

    def parse_program(self, tokens):
        self.tokens = tokens
        self.body = []

        while (not helper.is_eof(self.index, self.tokens)):
            stmt = self.parse_statement()

            self.body.append(stmt)

        return nodes.Program(body=self.body)

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
        elif (current_token["value"] == Keywords.IF):
            return self.parse_if()
        # elif (current_token["type"] == "IDENTIFIER" or current_token["type"] == "NUMBER"):
        else:
            return self.parse_expression()

        # raise TypeError(f"Unknown statement starting with {self.peek()["value"]}")

    def parse_var(self):
        self.match(Keywords.VAR, "value")
        identifier = self.match("IDENTIFIER", "type")
        self.match(Operators.EQUAL, "value")
        expression = self.parse_expression()

        return nodes.VariableDeclaration(declaration=nodes.VariableDeclarator(id=nodes.Identifier(name=identifier["value"]), init=expression))
    
    def parse_set(self):
        self.match(Keywords.SET, "value")
        postfix = self.parse_postfix()
        operator = self.match_assignment()
        expression = self.parse_expression()

        return nodes.VariableAssignment(operator=operator, declaration=nodes.VariableDeclarator(id=postfix, init=expression))

    def parse_function(self):
        self.match(Keywords.PRC, "value")
        identifier = self.match("IDENTIFIER", "type")
        self.match(Punctuations.PARANTHESSES_O, "value")
        params = self.parse_params()
        self.match(Punctuations.PARANTHESSES_C, "value")
        body = self.parse_block()

        return nodes.FunctionDeclaration(nodes.Identifier(identifier["value"]), params, body)
    
    def parse_if(self):
        self.match(Keywords.IF, "value")
        self.match(Punctuations.PARANTHESSES_O, "value")
        condition = self.parse_expression()
        self.match(Punctuations.PARANTHESSES_C, "value")
        body = self.parse_block()
        alternate = self.parse_alternate()

        # parse maybe
        # parse else

        return nodes.IfStatement(condition, body, alternate)
    
    def parse_alternate(self):
        if (not helper.is_eof(self.index, self.tokens)):
            if (self.peek()["value"] == Keywords.MAYBE):
                self.match(Keywords.MAYBE, "value")
                self.match(Punctuations.PARANTHESSES_O, "value")
                condition = self.parse_expression()
                self.match(Punctuations.PARANTHESSES_C, "value")
                body = self.parse_block()

                alternate = self.parse_alternate()

                return nodes.IfStatement(condition, body, alternate)
            elif (self.peek()["value"] == Keywords.WHATEVER):
                self.match(Keywords.WHATEVER, "value")
                body = self.parse_block()

                return nodes.IfStatement(None, body, None)
            else:
                return None
    
    def parse_block(self):
        self.match(Punctuations.CURVED_O, "value")
        
        body = []

        while (self.peek()["value"] != Punctuations.CURVED_C):
            statement = self.parse_statement()

            body.append(statement)

        self.match(Punctuations.CURVED_C, "value")

        return nodes.BlockStatement(body)
    
    def parse_params(self):
        params = []

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["type"] == "IDENTIFIER"):
            param = self.match("IDENTIFIER", "type")["value"]

            params.append(nodes.Identifier(param))

            if (self.peek()["value"] != Punctuations.PARANTHESSES_C):
                self.match(Punctuations.COMMA, "value")

        return params
    
    def parse_args(self):
        args = []

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] != Punctuations.PARANTHESSES_C):
            arg = self.parse_expression()

            args.append(arg)

            if (self.peek()["value"] != Punctuations.PARANTHESSES_C):
                self.match(Punctuations.COMMA, "value")

        return args
    
    def parse_return(self):
        self.match(Keywords.RETURN, "value")
        expr = self.parse_expression()

        return nodes.ReturnStatement(expr)

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node_logical_and = self.parse_logical_and()

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] == Operators.OR):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_logical_and()
            
            node_logical_and = nodes.BinaryExpression(node_logical_and, current["value"], right)

        return node_logical_and

    def parse_logical_and(self):
        node_equality = self.parse_equality()

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] == Operators.AND):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_equality()
            
            node_equality = nodes.BinaryExpression(node_equality, current["value"], right)

        return node_equality

    def parse_equality(self):
        node_comparison = self.parse_comparison()

        while (not helper.is_eof(self.index, self.tokens) 
               and self.peek()["value"] in (
                   Operators.D_EQUAL, 
                   Operators.N_EQUAL
                )):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_comparison()
            
            node_comparison = nodes.BinaryExpression(node_comparison, current["value"], right)

        return node_comparison

    def parse_comparison(self):
        node_additive = self.parse_additive()

        while (not helper.is_eof(self.index, self.tokens) 
               and self.peek()["value"] in (
                   Operators.GREATER, 
                   Operators.LESS, 
                   Operators.G_EQUAL, 
                   Operators.L_EQUAL
                )):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_additive()
            
            node_additive = nodes.BinaryExpression(node_additive, current["value"], right)

        return node_additive

    def parse_additive(self):
        node_multiplicative = self.parse_multiplicative()

        while (not helper.is_eof(self.index, self.tokens) 
                and self.peek()["value"] in (
                    Operators.SUBTRACTION, 
                    Operators.ADDITION
                )):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_multiplicative()
            
            node_multiplicative = nodes.BinaryExpression(node_multiplicative, current["value"], right)

        return node_multiplicative

    def parse_multiplicative(self):
        node_power = self.parse_power()

        while (not helper.is_eof(self.index, self.tokens) 
               and self.peek()["value"] in (
                   Operators.MULTIPLICATION, 
                   Operators.DIVISION, 
                   Operators.MODULO
                )):
            current = self.match(self.peek()["value"], "value")
            right = self.parse_power()
            
            node_power = nodes.BinaryExpression(node_power, current["value"], right)

        return node_power

    def parse_power(self):
        node_unary = self.parse_unary()

        if (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] == Operators.POWER):
            operator = self.match(Operators.POWER, "value")
            right = self.parse_power()

            return nodes.BinaryExpression(node_unary, operator["value"], right)

        return node_unary
    
    def parse_unary(self):
        if (not helper.is_eof(self.index, self.tokens) 
            and self.peek()["value"] in (
                Operators.NEGATION, 
                Operators.ADDITION, 
                Operators.SUBTRACTION
            )):
            operator = self.match(self.peek()["value"], "value")
            right = self.parse_unary()

            return nodes.UnaryExpression(operator["value"], right)

        return self.parse_postfix()
    
    def parse_postfix(self):
        left = self.parse_atom()

        while (not helper.is_eof(self.index, self.tokens) 
               and self.peek()["value"] in (
                   Punctuations.SQUARE_O,
                   Punctuations.PARANTHESSES_O
                )):
            paran = self.match(self.peek()["value"], "value")

            if (paran["value"] == Punctuations.PARANTHESSES_O):
                args = self.parse_args()
                self.match(Punctuations.PARANTHESSES_C, "value")

                left = nodes.CallExpression(left, args)
            elif (paran["value"]  == Punctuations.SQUARE_O):
                f_exp = self.parse_expression()
                s_exp = None

                if (self.peek()["value"] == Punctuations.COLON):
                    self.match(Punctuations.COLON, "value")
                    s_exp = self.parse_expression()

                self.match(Punctuations.SQUARE_C, "value")

                left = nodes.PostfixExpression(left, f_exp, s_exp)

        return left
    
    def parse_atom(self):
        current = self.peek()
        
        if (current["type"] in ("STRING", "NUMBER") 
            or (current["type"] == "KEYWORDS" 
                and current["value"] in ("true", "false", "empty", "undefined"))):
            return self.parse_literal()
        elif (current["type"] == "IDENTIFIER"):
            self.match("IDENTIFIER", "type")

            return nodes.Identifier(current["value"])
        elif (current["value"] == "("):
            self.match(Punctuations.PARANTHESSES_O, "value")
            expr = self.parse_expression()
            self.match(Punctuations.PARANTHESSES_C, "value")

            return nodes.GroupedExpression(Punctuations.PARANTHESSES_O, expr, Punctuations.PARANTHESSES_C)
        elif (current["value"] == Punctuations.SQUARE_O):
            return self.parse_list()
        elif (current["value"] == Punctuations.CURVED_O):
            return self.parse_hashmap()

        raise TypeError(f"Expected atom, but got {current["value"]}")

    def parse_list(self):
        expr_lst = []
        
        self.match(Punctuations.SQUARE_O, "value")
        
        while (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] != Punctuations.SQUARE_C):
            if (self.peek()["value"] == Punctuations.SQUARE_O):
                expr = self.parse_list()
            else:
                expr = self.parse_expression()

            expr_lst.append(expr)

            if (self.peek()["value"] != Punctuations.SQUARE_C):
                self.match(Punctuations.COMMA, "value")

        self.match(Punctuations.SQUARE_C, "value")

        return nodes.ListExpression(expr_lst)

    def parse_hashmap(self):
        self.match(Punctuations.CURVED_O, "value")
        
        items = { }

        while (not helper.is_eof(self.index, self.tokens) and self.peek()["value"] != Punctuations.CURVED_C):
            key = self.parse_expression()
            self.match(":", "value")
            value = self.parse_expression()

            items[key] = value

            if (self.peek()["value"] != Punctuations.CURVED_C):
                self.match(Punctuations.COMMA, "value")

        self.match(Punctuations.CURVED_C, "value")

        return nodes.HashmapExpression(items)
    
    def parse_literal(self):
        current = self.peek()

        if (current["type"] == "STRING"):
            return self.parse_string()
        elif (current["type"] == "NUMBER"):
            return self.parse_number()
        elif (current["type"] == "KEYWORDS" and current["value"] in ("true", "false")):
            return self.parse_boolean()
        elif (current["type"] == "KEYWORDS" and current["value"] == "empty"):
            return self.parse_empty()
        elif (current["type"] == "KEYWORDS" and current["value"] == "undefined"):
            return self.parse_undefined()

    def parse_string(self):
        value = self.match("STRING", "type")["value"]

        return nodes.Literal(value)

    def parse_number(self):
        value = self.match("NUMBER", "type")["value"]

        return nodes.Literal(value)

    def parse_boolean(self):
        value = self.match(self.peek()["value"], "value")["value"]

        return nodes.Literal(value)

    def parse_empty(self):
        self.match(Keywords.EMPTY, "value")

        return nodes.Literal(Keywords.EMPTY)
    
    def parse_undefined(self):
        self.match(Keywords.UNDEFINED, "value")

        return nodes.Literal(Keywords.UNDEFINED)

def main():
    parser = Parser()

    sample = [
        {"type": "KEYWORDS", "value": "var"},
        {"type": "IDENTIFIER", "value": "x"},
        {"type": "OPERATOR", "value": "="},
        {"type": "OPERATOR", "value": "-"},
        {"type": "NUMBER", "value": "6"},
        {"type": "OPERATOR", "value": "<"},
        {"type": "NUMBER", "value": "2"},
    ]

    for token in parser.parse_program(sample).body:
        print(repr(token))


if __name__ == "__main__":
    main()
