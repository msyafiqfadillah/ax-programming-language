from environment import Environment
from nodes import *
from gtypes import *
from tokens.operators import Operators

class TypeChecker:
    def __init__(self):
        self.env = global_env

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
            id = stmt.name
            param_type = [ttp["type"] for ttp in stmt.params]
            return_type = stmt.return_type
            fc_type = FunctionType(param_type, return_type)

            self.env.define(id, fc_type)
        elif (isinstance(stmt, IfStatement)):
            if ((stmt.condition is not None)
                    and not isinstance(self.check_expression(stmt.condition), BooleanType)):
                raise TypeError("Condition must be a boolean type")

            local_env = Environment({}, self.env)
            self.check_block(stmt.body, local_env)

            if (stmt.alternate is not None):
                self.check_statement(stmt.alternate)
        elif (isinstance(stmt, LoopStatement)):
            pass

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
