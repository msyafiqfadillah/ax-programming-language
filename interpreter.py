from environment import Environment
from scanner import Scanner
from parser import Parser, VariableDeclaration, BinaryExpression, Identifier, Literal, GroupedExpression, FunctionDeclaration


class Interpreter:
    def __init__(self):
        self.env = Environment({})

    def run(self, source):
        tokens = Scanner().scans(source)
        ast = Parser().parse_program(tokens)

        for stmt in ast.body:
            self.eval_statement(stmt)

        return self.env.record

    def eval_statement(self, stmt):
        if (isinstance(stmt, VariableDeclaration)):
            name = stmt.declaration.id.name
            value = self.eval_expression(stmt.declaration.init)

            if (stmt.kind == "var"):
                if (name in self.env.record):
                    raise NameError(f"Variable '{name}' already declared")

                self.env.record[name] = value
                
                return value
            elif (stmt.kind == "set"):
                if (name not in self.env.record):
                    raise NameError(f"Variable '{name}' is not defined")

                self.env.record[name] = value

                return value
        elif (isinstance(stmt, FunctionDeclaration)):
            pass

        # expression statements
        return self.eval_expression(stmt)

    def eval_expression(self, expr):
        if (isinstance(expr, Literal)):
            v = expr.value

            # try to convert numeric strings to numbers
            if (isinstance(v, str)):
                try:
                    if ("." in v):
                        return float(v)
                    return int(v)
                except Exception:
                    return v

            return v

        if (isinstance(expr, Identifier)):
            name = expr.name
            
            if (name in self.env.record):
                return self.env.record[name]
            
            raise NameError(f"Variable '{name}' is not defined")

        if (isinstance(expr, GroupedExpression)):
            return self.eval_expression(expr.expr)

        if (isinstance(expr, BinaryExpression)):
            left = self.eval_expression(expr.left)
            right = self.eval_expression(expr.right)
            op = expr.operator

            if (op == "+"):
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                
                return left + right
            if (op == "-"):
                return left - right
            if (op == "*"):
                return left * right
            if (op == "/"):
                return left / right
            if (op == "%"):
                return left % right
            if (op == "^"):
                return left ** right

            if (op == ">="):
                return left >= right
            if (op == "<="):
                return left <= right
            if (op == "=="):
                return left == right
            if (op == "!="):
                return left != right
            if (op == ">"):
                return left > right
            if (op == "<"):
                return left < right

            raise TypeError(f"Unknown operator {op}")

        raise TypeError(f"Unknown expression type: {expr}")


def main():
    # sample = '''
    #     var x = 42
    #     var y = 99
    #     var z = x + (y + 3)
    #     var _g = "ABC"

    #     set x = 32 % 2
    #     set x = y * z + 22

    #     fct test(param_1, param_2) {
    #         var b = 123
    #     }
    # '''

    sample = '''
        var x = 42
        var y = 99
        var z = x + (y + 3)
        var _g = "ABC"

        set x = 32 % 2
        set x = y * x + 22
    '''

    interp = Interpreter()
    env = interp.run(sample)
    print(env)


if (__name__ == "__main__"):
    main()