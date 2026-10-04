import nodes

from tokens.operators import Operators
from environment import Environment
from scanner import Scanner
from parser import Parser
from values import (
    StringValue, NumberValue, EmptyValue,
    ListValue, HashmapValue, BuiltinValue,
    FunctionValue, BooleanValue
)


class ReturnException(Exception):
    def __init__(self):
        pass

class ContinueException(Exception):
    def __init__(self):
        pass

class BreakException(Exception):
    def __init__(self):
        pass

class Interpreter:
    def __init__(self):
        self.env = global_env
        self.loop_depth = 0

    def run(self, source):
        tokens = Scanner().scans(source)
        ast = Parser().parse_program(tokens)

        for stmt in ast.body:
            self.eval_statement(stmt)

        return self.env.record

    def resolve_assignment(self, node):
        if (isinstance(node, nodes.Identifier)):
            name = node.name

            if (self.env.resolve(name)):
                return ("env", name)
            else:
                raise NameError(f"Variable {name} is not defined")

        if (isinstance(node, nodes.PostfixExpression)):
            container, key = self.resolve_assignment(node.exp)

            if (container == "env"):
                parent_value = self.env.lookup(key)
            else:
                if (isinstance(container, ListValue)):
                    parent_value = container.indexAt(self, key)
                elif (isinstance(container, HashmapValue)):
                    parent_value = container.valueAt(self, key)

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
            name = stmt.declaration.id.name
            value = self.eval_expression(stmt.declaration.init)

            if (name in self.env.record):
                raise NameError(f"Variable '{name}' already declared")

            self.env.define(name, value)

            return value
        elif (isinstance(stmt, nodes.VariableAssignment)):
            id = stmt.declaration.id
            container, key = self.resolve_assignment(id)
            value = self.eval_expression(stmt.declaration.init)

            if (container == "env"):
                old_value = self.env.lookup(key)

                if (not old_value.type.is_assignable(value.type)):
                    raise RuntimeError(f"Cannot assign value of type {value.type} to variable of type {old_value.type}")
            else:
                if (isinstance(container, ListValue)):
                    old_value = container.indexAt(self, key)
                elif (isinstance(container, HashmapValue)):
                    old_value = container.valueAt(self, key)

            if (stmt.operator["value"] == Operators.A_EQUAL):
                value = NumberValue(old_value.value + value.value)
            elif (stmt.operator["value"] == Operators.M_EQUAL):
                value = NumberValue(old_value.value * value.value)
            elif (stmt.operator["value"] == Operators.S_EQUAL):
                value = NumberValue(old_value.value - value.value)
            elif (stmt.operator["value"] == Operators.D_EQUAL):
                value = NumberValue(old_value.value / value.value)
            elif (stmt.operator["value"] == Operators.P_EQUAL):
                value = NumberValue(old_value.value ** value.value)
            elif (stmt.operator["value"] == Operators.MO_EQUAL):
                value = NumberValue(old_value.value % value.value)

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
        elif (isinstance(stmt, nodes.IfStatement)):
            if ((stmt.condition is None) or (self.eval_expression(stmt.condition).value)):
                local_env = Environment({}, self.env)

                self.eval_block(stmt.body, local_env)
            else:
                if (isinstance(stmt.alternate, nodes.IfStatement)):
                    self.eval_statement(stmt.alternate)

            return
        elif (isinstance(stmt, nodes.LoopStatement)):
            self.loop_depth += 1

            try:
                while (self.eval_expression(stmt.condition).value):
                    try:
                        local_env = Environment({}, self.env)

                        self.eval_block(stmt.body, local_env)
                    except ContinueException:
                        continue
                    except BreakException:
                        break
            finally:
                self.loop_depth -= 1

            return
        elif (isinstance(stmt, nodes.ContinueStatement)):
            if (self.loop_depth == 0):
                raise RuntimeError("Cannot use continue outside loop statement")

            raise ContinueException()
        elif (isinstance(stmt, nodes.BreakStatement)):
            if (self.loop_depth == 0):
                raise RuntimeError("Cannot use break outisde loop statement")

            raise BreakException()

        # expression statements
        return self.eval_expression(stmt)

    def eval_expression(self, expr):
        if (isinstance(expr, nodes.Literal)):
            value = expr.value
            type_value = expr.type

            match type_value:
                case "BOOLEAN":
                    return BooleanValue(value)
                case "NUMBER":
                    return NumberValue(value)
                case "STRING":
                    return StringValue(value)
                case "EMPTY":
                    return EmptyValue()

        if (isinstance(expr, nodes.Identifier)):
            _, key = self.resolve_assignment(expr)
            value = self.env.lookup(key)

            return self.eval_expression(value)

        if (isinstance(expr, nodes.GroupedExpression)):
            return self.eval_expression(expr.expr)

        if (isinstance(expr, nodes.BinaryExpression)):
            left = self.eval_expression(expr.left)
            right = self.eval_expression(expr.right)
            op = expr.operator

            if (op == Operators.ADDITION):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value + right.value)
            elif (op == Operators.SUBTRACTION):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value - right.value)
            elif (op == Operators.MULTIPLICATION):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value * right.value)
            elif (op == Operators.DIVISION):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value / right.value)
            elif (op == Operators.MODULO):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value % right.value)
            elif (op == Operators.POWER):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return NumberValue(left.value ** right.value)
            elif (op == Operators.GREATER):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return BooleanValue(left.value > right.value)
            elif (op == Operators.LESS):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return BooleanValue(left.value < right.value)
            elif (op == Operators.G_EQUAL):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return BooleanValue(left.value >= right.value)
            elif (op == Operators.L_EQUAL):
                if (isinstance(left, NumberValue) and isinstance(right, NumberValue)):
                    return BooleanValue(left.value <= right.value)
            elif (op == Operators.E_EQUAL):
                if (isinstance(left, (BooleanValue, StringValue, NumberValue)) and isinstance(right, (BooleanValue, StringValue, NumberValue))):
                    return BooleanValue(left.value == right.value)
            elif (op == Operators.N_EQUAL):
                if (isinstance(left, (BooleanValue, StringValue, NumberValue)) and isinstance(right, (BooleanValue, StringValue, NumberValue))):
                    return BooleanValue(left.value != right.value)
            elif (op == Operators.AND):
                if (isinstance(left, (BooleanValue, StringValue, NumberValue)) and isinstance(right, (BooleanValue, StringValue, NumberValue))):
                    return BooleanValue(left.value and right.value)
            elif (op == Operators.OR):
                if (isinstance(left, (BooleanValue, StringValue, NumberValue)) and isinstance(right, (BooleanValue, StringValue, NumberValue))):
                    return BooleanValue(left.value or right.value)

            raise TypeError(f"Operation with '{op}' is invalid between {type(left).__name__} and {type(right).__name__}")

        if (isinstance(expr, nodes.UnaryExpression)):
            op = expr.operator
            right = self.eval_expression(expr.value)

            if (op == "+"):
                if (isinstance(right, NumberValue)):
                    return NumberValue(+right.value)
            elif (op == "-"):
                if (isinstance(right, NumberValue)):
                    return NumberValue(-right.value)
            elif (op == "!"):
                return BooleanValue(not right.value)

        if (isinstance(expr, nodes.CallExpression)):
            if (isinstance(expr.callee, nodes.CallExpression)):
                result = self.eval_expression(expr.callee)
            else:
                result = self.env.lookup(expr.callee.name)

            result = result.call(self, [self.eval_expression(arg) for arg in expr.arguments])

            return result

        if (isinstance(expr, nodes.FunctionExpression)):
            func = FunctionValue(expr.params, expr.body, self.env)

            return func

        if (isinstance(expr, nodes.ListExpression)):
            return ListValue([self.eval_expression(e) for e in expr.value])

        if (isinstance(expr, nodes.HashmapExpression)):
            return HashmapValue({self.eval_expression(key).value : self.eval_expression(value) for key, value in expr.value.items()})

        if (isinstance(expr, nodes.PostfixExpression)):
            eval_expr = self.eval_expression(expr.exp)
            start_exp = self.eval_expression(expr.start_exp)

            if (isinstance(eval_expr, ListValue)):
                if (not expr.end_exp):
                    return eval_expr.indexAt(self, start_exp)
                else:
                    end_exp = self.eval_expression(expr.end_exp)

                    return eval_expr.slice(self, start_exp, end_exp)
            elif (isinstance(eval_expr, HashmapValue)):
                return eval_expr.valueAt(self, start_exp)

        if (isinstance(expr, (FunctionValue, ListValue, HashmapValue, BooleanValue, NumberValue, StringValue, EmptyValue))):
            return expr

        raise TypeError(f"Unknown expression type: {expr}")


global_env = Environment({
    "show": BuiltinValue(lambda *args : print(*args)),
    "length": BuiltinValue(lambda arg : len(arg.value)),
    "push": BuiltinValue(lambda list_value, *args : list(map(list_value.push, args)))
})


def main():
    # sample = '''
    #     ~ This is a example of comment ~
    #     ~
    #         You can use it as one line comment or multiline,
    #         like this.
    #     ~
    #     # Or you can use hashtag as one line comment

    #     prc x() {
    #         prc z() {
    #             return [[1, 2, 3, 100, 99, 98], [44, 33, 12]]
    #         }

    #         return z
    #     }

    #     prc o() {
    #         return 222
    #     }

    #     var p = [1, 2, 3, 4]
    #     var g = x()()

    #     ~ show(x()()[0:3][1][0:2][0]) ~
    #     show(g[0])

    #     set g[0][1] = [9, 0, 7]

    #     show(g)
    #     # push(g[0][1], 22)
    #     # show(g)

    #     var ttt = { "123" : 123, "uuu" : 999 }

    #     show(ttt["123"])

    #     set ttt["123"] = 5000

    #     show(ttt)
    #     push(g[0][1], 22)
    #     show(g)

    #     ~
    #         example of if else in ax (written with neovim)
    #     ~

    #     var nine = 9
    #     var eight = 8

    #     if (nine >= eight) {
    #         show("yes, it's bigger")
    #     } maybe (nine <= eight) {
    #         show("no, it's not bigger")
    #     } maybe (nine == eight) {
    #         show("also not equal")
    #     } whatever {
    #         show("how?!")
    #     }

    #     ~
    #         testing assignment operator
    #     ~

    #     var mmx = 10
    #     set mmx += 1
    #     set mmx *= 100

    #     var zzm = { "a": 90, "b": 77 }
    #     set zzm["a"] += 10

    #     var lst = [10, 11, 90, 91]
    #     set lst[2] -= 81

    #     show(lst)

    #     ~
    #         testing loop statement
    #     ~
    #     ~
    #     var mgmt = [1, 9, 90, 190, 1990]
    #     var l_mgmt = length(mgmt)
    #     var index = 0
    #     var xxx = 0

    #     loop (index < l_mgmt) {
    #         show(mgmt[index])

    #         set xxx = 0

    #         loop (xxx < 3) {
    #             if (xxx % 2 == 0) {
    #                 continue
    #             }

    #             show(xxx)

    #             set xxx += 1
    #         }

    #         set index += 1
    #     }
    #     ~
    #     var oo = 0

    #     loop (oo < 5) {
    #         if (oo == 3) {
    #             set oo += 1

    #             continue
    #         } maybe (oo == 4) {
    #             break
    #         }

    #         show(oo)

    #         set oo += 1
    #     }

    #     ~
    #         testing lambda function
    #     ~
    #     var ggh = prc () {
    #         show("testing", oo)
    #     }

    #     ggh()
    # '''

    sample = '''
        var x = 10

        set x = "abc"

        show(x)
    '''

    interp = Interpreter()
    interp.run(sample)


if (__name__ == "__main__"):
    main()
