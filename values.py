from gtypes import (
        FunctionType, HashmapType, ListType,
        StringType, NumberType, EmptyType,
        BooleanType, AnyType, unify_types
)
from environment import Environment

class Value:
    def __init__(self, type):
        self.type = type

    def get_type(self):
        return self.type

class FunctionValue(Value):
    def __init__(self, params, body, parent_env):
        self.params = params
        self.body = body
        self.parent_env = parent_env

        if (len(self.params) > 0):
            tp = [AnyType() for _ in range(len(self.params))]
        else:
            tp = [EmptyType()]

        super().__init__(FunctionType(tp, AnyType()))

    def call(self, interpreter, args):
        if (len(args) != len(self.params)):
            raise RuntimeError(f"{self.params[-1]} is needed!")

        for param, arg in zip(self.type.param_types, args):
            if (not param.is_assignable(arg.type)):
                raise RuntimeError("Type mismatch!")

        local_env = Environment({}, self.parent_env)
        current_loop_state = interpreter.loop_depth

        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)

        interpreter.loop_depth = 0

        try:
            result = interpreter.eval_block(self.body, local_env)
        finally:
            interpreter.loop_depth = current_loop_state

        if (result is not None):
            self.type = FunctionType([arg.type for arg in args], result.type)

        return result

class BuiltinValue:
    def __init__(self, func):
        self.func = func

    def call(self, interpreter, args):
        return self.func(*args)

class ListValue(Value):
    def __init__(self, value):
        self.value = value

        super().__init__(ListType(self.__get_value_type()))

    def __get_value_type(self):
        return unify_types([tp.type for tp in self.value])

    def indexAt(self, interpreter, index):
        if (isinstance(index, NumberValue)):
            return self.value[interpreter.eval_expression(index).value]

        return None

    def replaceAt(self, index, value):
        if (isinstance(index, NumberValue)):
            if (self.type.type.is_assignable(value.type)):
                self.value[index.value] = value
            else:
                raise RuntimeError(f"Cannot assign {value.type} to {self.value[index.value].type}")

    def slice(self, interpreter, start, end):
        if (isinstance(start, NumberValue) and isinstance(end, NumberValue)):
            return ListValue(self.value[interpreter.eval_expression(start):interpreter.eval_expression(end)])

        return None

    def push(self, value):
        self.value.append(value)

    def __repr__(self):
        rep = f"[ {", ".join([str(expr) for expr in self.value])} ]"

        return rep

class HashmapValue(Value):
    def __init__(self, value):
        self.value = value

        super().__init__(HashmapType(self.__get_value_type()))

    def __get_value_type(self):
        return unify_types([tp.type for tp in self.value.values()])

    def valueAt(self, interpreter, key):
        return self.value[interpreter.eval_expression(key).value]

    def replaceAt(self, key, value):
        if (isinstance(key, StringValue)):
            if (self.type.type.is_assignable(value.type)):
                self.value[key.value] = value
            else:
                raise RuntimeError(f"Cannot assign {value.type} to {self.value[key.value].type}")

    def __repr__(self):
        rep = "{ " + f"{", ".join([f"{key} : {value}" for key, value in self.value.items()])}" + " }"

        return rep

class BooleanValue(Value):
    def __init__(self, value):
        super().__init__(BooleanType())

        self.value = value

    def __repr__(self):
        return str(self.value).lower()

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class NumberValue(Value):
    def __init__(self, value):
        super().__init__(NumberType())

        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class StringValue(Value):
    def __init__(self, value):
        super().__init__(StringType())

        self.value = value

    def __repr__(self):
        return f"\"{self.value}\""

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class EmptyValue(Value):
    def __init__(self):
        super().__init__(EmptyType())

        self.value = None

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

if (__name__ == "__main__"):
    # x = HashmapValue({
    #         "a" : ListValue([ NumberValue(123), NumberValue(999) ]),
    #         "b" : ListValue([ HashmapValue({ "a": NumberValue(123), "b": NumberValue(999) }) ])
    #     })

    # x = ListValue([
    #     ListValue([ ListValue([ NumberValue(123), NumberValue(999) ]) ]),
    #     ListValue([ ListValue([ StringValue(888), NumberValue(111) ]) ])
    # ])

    # x = ListValue([
    #     HashmapValue({ "a": NumberValue(123), "b": NumberValue(999) }),
    #     HashmapValue({ "a": NumberValue(123), "b": NumberValue(999) })
    # ])

    # x = FunctionValue([
    #     NumberValue(123), NumberValue(999)
    # ], { "return 123" }, {})

    # print(x.type)
    pass
