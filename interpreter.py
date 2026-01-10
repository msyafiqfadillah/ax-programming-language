from environment import Environment
from scanner import Scanner
from parser import Parser, VariableDeclaration, BinaryExpression, Identifier, Literal, GroupedExpression, FunctionDeclaration, CallExpression


class FunctionMap:
    def __init__(self, params, body, parent_env):
        self.params = params 
        self.body = body
        self.parent_env = parent_env
    def call(self, interpreter, args):
        if (len(args) != len(self.params)):
            raise RuntimeError(f"{self.params[-1]} is needed!")

        # TODO: return statement

        local_env = Environment({}, interpreter.env)

        for param, arg in zip(self.params, args):
            local_env.define(param, arg)

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
            self.eval_statement(stmt)

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
        
        if (isinstance(expr, CallExpression)):
            name = expr.callee.name
            result = self.env.lookup(name).call(self, expr.arguments)

            return result

        raise TypeError(f"Unknown expression type: {expr}")


def main():
    sample = '''
        var x = 42
        var y = 99
        var z = x + (y + 3)
        var _g = "ABC"

        set x = 32 % 2
        set x = y * z + 22

        prc test(param_1, param_2) {
            var b = 123
        }

        test(10)
    '''

    # sample = '''
    #     var x = 42
    #     var y = 99
    #     var z = x + (y + 3)
    #     var _g = "ABC"

    #     set x = 32 % 2
    #     set x = y * x + 22
    # '''

    interp = Interpreter()
    env = interp.run(sample)
    print(env)


if (__name__ == "__main__"):
    main()