from environment import Environment
from nodes import *
from gtypes import *
from tokens.operators import Operators

class TypeChecker:
    def __init__(self):
        self.env = global_env
        self.current_return_type = None

    def check(self, ast):
        for stmt in ast.body:
            self.check_statement(stmt)

    def resolve_assignment(self, node):
        if (isinstance(node, Identifier)):
            name = node.name

            if (self.env.resolve(name)):
                return self.env.lookup(name)
            else:
                raise NameError(f"Variable {name} is not defined")
        elif (isinstance(node, PostfixExpression)):
            container_type = self.resolve_assignment(node.exp)
            index_type = self.check_expression(node.start_exp)

            if (isinstance(container_type, ListType)):
                if (not isinstance(index_type, NumberType)):
                    raise TypeError(f"Index type must be number, got {index_type}")

                return container_type.type
            elif (isinstance(container_type, HashmapType)):
                if (not isinstance(index_type, StringType)):
                    raise TypeError(f"Key type must be string, got {index_type}")

                return container_type.type
            else:
                raise TypeError(f"Type {container_type} isn't indexable")
        else:
            raise TypeError("Invalid assignment target")

    def check_block(self, stmts, local_env):
        parent_block = self.env
        self.env = local_env

        try:
            for stmt in stmts.body:
                self.check_statement(stmt)
        finally:
            self.env = parent_block

    def check_statement(self, stmt):
        if (isinstance(stmt, VariableDeclaration)):
            name = stmt.declaration.id.name
            type = stmt.type
            value_type = self.check_expression(stmt.declaration.init)

            if ((type != value_type) or (not type.is_assignable(value_type))):
                raise TypeError(f"{value_type} cannot be assign to {type}")
            else:
                self.env.define(name, type)
        elif (isinstance(stmt, VariableAssignment)):
            id = stmt.declaration.id
            id_type = self.resolve_assignment(id)
            value_type = self.check_expression(stmt.declaration.init)

            if (not id_type.is_assignable(value_type)):
                raise TypeError(f"{value_type} cannot assign to {id_type}")
        elif (isinstance(stmt, FunctionDeclaration)):
            id = stmt.name.name
            params = { x["name"].name: x["type"] for x in stmt.params }
            param_type = params.values()
            return_type = stmt.return_type
            fc_type = FunctionType(param_type, return_type)

            self.env.define(id, fc_type)

            prev_return_type = self.current_return_type
            self.current_return_type = return_type

            local_env = Environment(params, self.env)
            self.check_block(stmt.body, local_env)

            self.current_return_type = prev_return_type
        elif (isinstance(stmt, IfStatement)):
            if ((stmt.condition is not None)
                    and not isinstance(self.check_expression(stmt.condition), BooleanType)):
                raise TypeError("Condition must be a boolean type")

            local_env = Environment({}, self.env)
            self.check_block(stmt.body, local_env)

            if (stmt.alternate is not None):
                self.check_statement(stmt.alternate)
        elif (isinstance(stmt, LoopStatement)):
            condition_type = self.check_expression(stmt.condition)

            if (not isinstance(condition_type, BooleanType)):
                raise TypeError("Condition must be a boolean type")

            local_env = Environment({}, self.env)
            self.check_block(stmt.body, local_env)
        elif (isinstance(stmt, ReturnStatement)):
            # TODO: handle void return type

            if (self.current_return_type is None):
                raise RuntimeError("Cannot use return outside function")

            actual_type = self.check_expression(stmt.argument)

            if (not self.current_return_type.is_assignable(actual_type)):
                raise TypeError(f"Cannot return {actual_type} from function expecting {self.current_return_type}")
        else:
            self.check_expression(stmt)

    def check_expression(self, expr):
        if (isinstance(expr, Literal)):
            return self.get_base(expr.type)

        if (isinstance(expr, Identifier)):
            return self.env.lookup(expr.name)

        if (isinstance(expr, GroupedExpression)):
            return self.check_expression(expr.expr)

        if (isinstance(expr, BinaryExpression)):
            left_type = self.check_expression(expr.left)
            operator = expr.operator
            right_type = self.check_expression(expr.right)

            if (operator in (
                Operators.E_EQUAL, Operators.G_EQUAL, Operators.N_EQUAL,
                Operators.L_EQUAL, Operators.POWER, Operators.MODULO,
                Operators.GREATER, Operators.LESS, Operators.OR, Operators.AND
            )):
                return BooleanType()
            elif (operator in (
                Operators.A_EQUAL, Operators.M_EQUAL, Operators.S_EQUAL,
                Operators.D_EQUAL, Operators.P_EQUAL, Operators.MO_EQUAL,
                Operators.ADDITION, Operators.MULTIPLICATION, Operators.SUBTRACTION,
                Operators.DIVISION, Operators.POWER, Operators.MODULO
            ) and (isinstance(left_type, NumberType)
                    and isinstance(right_type, NumberType))):
                return NumberType()

        if (isinstance(expr, UnaryExpression)):
            return self.check_expression(expr.value)

        if (isinstance(expr, ListExpression)):
            atype = list({self.check_expression(item) for item in expr.value})

            if (len(atype) > 0):
                return ListType(atype[0])
            else:
                return ListType(AnyType())

        if (isinstance(expr, HashmapExpression)):
            atype = list({self.check_expression(item) for item in expr.value})

            if (len(atype) > 0):
                return HashmapType(atype[0])
            else:
                return HashmapType(AnyType())

        if (isinstance(expr, FunctionExpression)):
            ps_type = [typ["type"] for typ in expr.params]
            r_type = expr.return_type

            return FunctionType(ps_type, r_type)

        if (isinstance(expr, CallExpression)):
            callee_type = self.check_expression(expr.callee)
            callee_name = expr.callee

            if (isinstance(callee_type, FunctionType)):
                params_len = len(callee_type.param_types)
                args_len = len(expr.arguments)

                if (args_len == params_len):
                    for ix, tx in enumerate(expr.arguments):
                        ct = callee_type.param_types[ix]
                        tp = self.check_expression(tx)

                        if (not ct.is_assignable(tp)):
                            raise TypeError(f"Cannot assign {tp} to {ct}")
                else:
                    raise TypeError(f"{callee_name} required {params_len} parameters, assign {args_len}")

                return callee_type.return_type
            else:
                raise TypeError(f"{callee_name} is not a function")

        if (isinstance(expr, PostfixExpression)):
            eval_exp = self.check_expression(expr.exp)
            start_exp = self.check_expression(expr.start_exp)

            if (isinstance(eval_exp, ListType)):
                if (expr.end_exp is not None):
                    if (not isinstance(start_exp, NumberType)):
                        raise TypeError("Start index must be integer")

                    end_exp = self.check_expression(expr.end_exp)

                    if (not isinstance(end_exp, NumberType)):
                        raise TypeError("End index must be integer")

                    return eval_exp
                else:
                    if (not isinstance(start_exp, NumberType)):
                        raise TypeError("List index must be integer")
            elif (isinstance(eval_exp, HashmapType)):
                if (not isinstance(start_exp, StringType)):
                    raise TypeError("Hashmap key must be string")
            else:
                raise TypeError(f"{eval_exp} isn't indexable")

            return eval_exp.type

    def get_base(self, value_type):
        match (value_type):
            case "STRING":
                return StringType()
            case "NUMBER":
                return NumberType()
            case "BOOLEAN":
                return BooleanType()
            case "EMPTY":
                return EmptyType()

global_env = Environment({})

def main():
    pass

if (__name__ == "__main__"):
    main()
