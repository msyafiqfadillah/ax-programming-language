from environment import Environment
from scanner import Scanner
from parser import Parser, VariableDeclaration, BinaryExpression, Identifier, Literal, GroupedExpression, FunctionDeclaration, ReturnStatement, CallExpression


class ReturnException(Exception):
    def __init__(self):
        pass

class FunctionMap:
    def __init__(self, params, body, parent_env):
        self.params = params 
        self.body = body
        self.parent_env = parent_env
    def call(self, interpreter, args):
        if (len(args) != len(self.params)):
            raise RuntimeError(f"{self.params[-1]} is needed!")

        local_env = Environment({}, interpreter.env)

        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)

        result = interpreter.eval_block(self.body, local_env)

        return result

class Interpreter:
    def __init__(self):
        self.env = Environment({})

    def run(self, source):
        tokens = Scanner().scans(source)
        ast = Parser().parse_program(tokens)

        for stmt in ast.body:
            self.eval_statement(stmt)

        return self.env.record
    
    def eval_block(self, stmts, local_env):
        parent_env = self.env
        self.env = local_env

        for stmt in stmts.body:
            try:
                self.eval_statement(stmt)

                return None
            except ReturnException:
                return self.eval_expression(stmt.argument)
            finally:
                self.env = parent_env

    def eval_statement(self, stmt):
        if (isinstance(stmt, VariableDeclaration)):
            name = stmt.declaration.id.name
            value = self.eval_expression(stmt.declaration.init)

            if (stmt.kind == "var"):
                if ((name in self.env.record) or (self.env.parent is not None and name in self.env.parent.record)):
                    raise NameError(f"Variable '{name}' already declared")

                self.env.define(name, value)
                
                return value
            elif (stmt.kind == "set"):
                if ((name not in self.env.record) or (self.env.parent is not None and name not in self.env.record)):
                    raise NameError(f"Variable '{name}' is not defined")

                self.env.define(name, value)

                return value
        elif (isinstance(stmt, FunctionDeclaration)):
            name = stmt.name.name
            func = FunctionMap(stmt.params, stmt.body, self.env)
            self.env.define(name, func)

            return func
        elif (isinstance(stmt, ReturnStatement)):
            if (self.env.parent is not None):
                raise ReturnException()
            else:
                raise RuntimeError("Cannot use return outside block")

        # expression statements
        return self.eval_expression(stmt)

    def eval_expression(self, expr):
        if (isinstance(expr, str) or isinstance(expr, int)):
            return expr

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
                return self.eval_expression(self.env.lookup(name))
            
            raise NameError(f"Variable '{name}' is not defined")

        if (isinstance(expr, GroupedExpression)):
            return self.eval_expression(expr.expr)

        if (isinstance(expr, BinaryExpression)):
            left = self.eval_expression(expr.left)
            right = self.eval_expression(expr.right)
            op = expr.operator

            if (op == "+"):
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
        
        if (isinstance(expr, CallExpression)):
            name = expr.callee.name
            result = self.env.lookup(name).call(self, expr.arguments)

            return result

        raise TypeError(f"Unknown expression type: {expr}")


def main():
    sample = '''
        var x = 42
        var y = 102
        var z = x + (y + 3)
        var _g = "ABC"

        set x = 32 % 7
        set x = y * x + 22

        prc test(param_1, param_2) {
            var b = 123
        }

        prc test_1(x1, x2) {
            return x1 + x2
        }

        test(10, 11)
        test_1(0, 3)
    '''

    interp = Interpreter()
    interp.run(sample)


if (__name__ == "__main__"):
    main()