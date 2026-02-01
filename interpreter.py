import helper
import nodes

from tokens.operators import Operators
from environment import Environment
from scanner import Scanner
from parser import Parser


class ReturnException(Exception):
    def __init__(self):
        pass

class FunctionValue:
    def __init__(self, params, body, parent_env):
        self.params = params 
        self.body = body
        self.parent_env = parent_env
        
    def call(self, interpreter, args):
        if (len(args) != len(self.params)):
            raise RuntimeError(f"{self.params[-1]} is needed!")

        local_env = Environment({}, self.parent_env)

        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)

        result = interpreter.eval_block(self.body, local_env)

        return result
    
class BuiltinMap:
    def __init__(self, func):
        self.func = func 

    def call(self, interpreter, args):
        evaluated_args = [interpreter.eval_expression(expr) for expr in args]

        return self.func(*evaluated_args)
    
class ListValue:
    def __init__(self, atoms):
        self.atoms = atoms 

    def operate(self, interpreter, start, end=None):
        if (end is None):
            return self.indexAt(interpreter, start)
        else:
            return self.slice(interpreter, start, end)

    def indexAt(self, interpreter, index):
        return self.atoms[interpreter.eval_expression(index)]
    
    def replaceAt(self, index, value):
        self.atoms[index] = value
    
    def slice(self, interpreter, start, end):
        return ListValue(self.atoms[interpreter.eval_expression(start):interpreter.eval_expression(end)])
    
    def __repr__(self):
        rep = f"[ {", ".join([str(expr) for expr in self.atoms])} ]"

        return rep

class Interpreter:
    def __init__(self):
        self.env = global_env

    def run(self, source):
        tokens = Scanner().scans(source)
        ast = Parser().parse_program(tokens)

        for stmt in ast.body:
            self.eval_statement(stmt)

        return self.env.record
    
    def resolve_assignment(self, node):
        if (isinstance(node, nodes.Identifier)):
            name = node.name

            if (not self.env.resolve(name)):
                raise NameError(f"Variable {name} is not defined")

            return ("env", name)
        
        if (isinstance(node, nodes.PostfixExpression)):
            container, key = self.resolve_assignment(node.exp)

            if (container == "env"):
                parent_value = self.env.lookup(key)
            else:
                parent_value = container.indexAt(self, key)

            index = self.eval_expression(node.start_exp)

            return (parent_value, index)
    
    def eval_block(self, stmts, local_env):
        parent_env = self.env
        self.env = local_env

        try:
            for stmt in stmts.body:
                self.eval_statement(stmt)
            
            return None
        except ReturnException:
            return self.eval_expression(stmt.argument)
        finally:
            self.env = parent_env

    def eval_statement(self, stmt):
        if (isinstance(stmt, nodes.VariableDeclaration)):
            id = stmt.declaration.id

            if (stmt.kind == "var"):
                name = id.name
                value = self.eval_expression(stmt.declaration.init)

                if ((name in self.env.record) or (self.env.parent is not None and name in self.env.parent.record)):
                    raise NameError(f"Variable '{name}' already declared")

                self.env.define(name, value)
                
                return value
            elif (stmt.kind == "set"):
                container, key = self.resolve_assignment(id)
                value = self.eval_expression(stmt.declaration.init)

                if (container == "env"):
                    self.env.assign(key, value)
                else:
                    container.replaceAt(key, value)

                return value
        elif (isinstance(stmt, nodes.FunctionDeclaration)):
            name = stmt.name.name
            func = FunctionValue(stmt.params, stmt.body, self.env)
            self.env.define(name, func)

            return func
        elif (isinstance(stmt, nodes.ReturnStatement)):
            if (self.env.parent is not None):
                raise ReturnException()
            else:
                raise RuntimeError("Cannot use return outside block")

        # expression statements
        return self.eval_expression(stmt)

    def eval_expression(self, expr):
        if (isinstance(expr, str) or isinstance(expr, int)):
            return expr

        if (isinstance(expr, nodes.Literal)):
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

        if (isinstance(expr, nodes.Identifier)):
            name = expr.name

            if ((name in self.env.record) or (self.env.parent is not None and name in self.env.parent.record)):
                return self.eval_expression(self.env.lookup(name))
            
            raise NameError(f"Variable '{name}' is not defined")

        if (isinstance(expr, nodes.GroupedExpression)):
            return self.eval_expression(expr.expr)

        if (isinstance(expr, nodes.BinaryExpression)):
            left = self.eval_expression(expr.left)
            right = self.eval_expression(expr.right)
            op = expr.operator

            if (op == Operators.ADDITION):
                return left + right
            if (op == Operators.SUBTRACTION):
                return left - right
            if (op == Operators.MULTIPLICATION):
                return left * right
            if (op == Operators.DIVISION):
                return left / right
            if (op == Operators.MODULO):
                return left % right
            if (op == Operators.POWER):
                return left ** right

            if (op == Operators.G_EQUAL):
                return helper.bool_converter(left >= right)
            if (op == Operators.L_EQUAL):
                return helper.bool_converter(left <= right)
            if (op == Operators.D_EQUAL):
                return helper.bool_converter(left == right)
            if (op == Operators.N_EQUAL):
                return helper.bool_converter(left != right)
            if (op == Operators.GREATER):
                return helper.bool_converter(left > right)
            if (op == Operators.LESS):
                return helper.bool_converter(left < right)
            
            if (op == Operators.OR):
                return helper.bool_converter(helper.is_truhty(left) or helper.is_truhty(right))
            if (op == Operators.AND):
                return helper.bool_converter(helper.is_truhty(left) and helper.is_truhty(right))

            raise TypeError(f"Unknown operator {op}")
        
        if (isinstance(expr, nodes.UnaryExpression)):
            op = expr.operator
            right = self.eval_expression(expr.value)

            if (op == "+"):
                return 0 + right
            if (op == "-"):
                return 0 - right
            if (op == "!"):
                return helper.bool_converter(not helper.is_truhty(right))
        
        if (isinstance(expr, nodes.CallExpression)):
            if (isinstance(expr.callee, nodes.CallExpression)):
                result = self.eval_expression(expr.callee)
            else:
                result = self.env.lookup(expr.callee.name)

            result = result.call(self, expr.arguments)

            return result
        
        if (isinstance(expr, nodes.ListExpression)):
            return ListValue([self.eval_expression(e) for e in expr.atoms])
        
        if (isinstance(expr, nodes.PostfixExpression)):
            return self.eval_expression(expr.exp).operate(self, expr.start_exp, expr.end_exp)

        if (isinstance(expr, (FunctionValue, ListValue))):
            return expr

        raise TypeError(f"Unknown expression type: {expr}")


global_env = Environment({
    "show": BuiltinMap(lambda *args : print(*args)),
    "length": BuiltinMap(lambda arg : len(arg))
})


def main():
    # sample = '''
    #     prc test() {
    #         var x = 10

    #         prc inner_test(new_param) {
    #             set x = x + new_param

    #             return x
    #         }

    #         return inner_test
    #     }

    #     var a = test()

    #     show(a(5))
    #     show(a(5))
    #     show(2 + 2)

    #     prc test() {
    #         var x = 10

    #         prc inner_test(new_param) {
    #             set x = x + new_param

    #             return x
    #         }

    #         return inner_test
    #     }

    #     var q = test()

    #     show(q(5))
    #     show(q(5))

    #     prc make_counter() {
    #         var count = 0
    #         prc inc() {
    #             set count = count + 1
    #             return count
    #         }
    #         return inc
    #     }

    #     var c1 = make_counter()
    #     var c2 = make_counter()

    #     show(c1())
    #     show(c1())
    #     show(c2())
    #     show(c1())
    # '''

    # sample = '''
    #     prc x() {
    #         return 555
    #     }

    #     var z = 10
    #     var m = [[1, 2, 3, x()], [777, 888]]

    #     show(m[0][0])
    # '''

    sample = '''
        prc x() {
            prc z() {
                return [[1, 2, 3, 100, 99, 98], [44, 33, 12]]
            }

            return z
        }

        prc o() {
            return 222
        }

        var p = [1, 2, 3, 4]
        var g = x()()

        show(x()()[0:3][1][0:2][0])
        show(g[0])

        set g[0][1] = [9, 0, 7]

        show(g)
    '''

    interp = Interpreter()
    interp.run(sample)


if (__name__ == "__main__"):
    main()