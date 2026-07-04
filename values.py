from environment import Environment

class FunctionValue:
    def __init__(self, params, body, parent_env):
        self.params = params 
        self.body = body
        self.parent_env = parent_env
        
    def call(self, interpreter, args):
        if (len(args) != len(self.params)):
            raise RuntimeError(f"{self.params[-1]} is needed!")

        local_env = Environment({}, self.parent_env)
        current_loop_state = interpreter.loop_depth

        for param, arg in zip(self.params, args):
            local_env.define(param.name, arg)

        interpreter.loop_depth = 0
        
        try:
            result = interpreter.eval_block(self.body, local_env)
        finally:
            interpreter.loop_depth = current_loop_state

        return result
    
class BuiltinValue:
    def __init__(self, func):
        self.func = func 

    def call(self, interpreter, args):
        evaluated_args = [interpreter.eval_expression(expr) for expr in args]

        return self.func(*evaluated_args)
    
class ListValue:
    def __init__(self, value):
        self.value = value

    def indexAt(self, interpreter, index):
        if (isinstance(index, NumberValue)):
            return self.value[interpreter.eval_expression(index).value]

        return None
    
    def replaceAt(self, index, value):
        if (isinstance(index, NumberValue)):
            self.value[index.value] = value

        return None
    
    def slice(self, interpreter, start, end):
        if (isinstance(start, NumberValue) and isinstance(end, NumberValue)):
            return ListValue(self.value[interpreter.eval_expression(start):interpreter.eval_expression(end)])

        return None

    def push(self, value):
        self.value.append(value)

    def __repr__(self):
        rep = f"[ {", ".join([str(expr) for expr in self.value])} ]"

        return rep
    
class HashmapValue:
    def __init__(self, value):
        self.value = value

    def valueAt(self, interpreter, key):
        return self.value[interpreter.eval_expression(key).value]
    
    def replaceAt(self, key, value):
        if (isinstance(key, StringValue)):
            self.value[key.value] = value

        return None

    def __repr__(self):
        rep = "{ " + f"{", ".join([f"{key} : {value}" for key, value in self.value.items()])}" + " }"

        return rep

class BooleanValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value).lower()

class NumberValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class StringValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"\"{self.value}\""

class EmptyValue:
    def __init__(self):
        self.value = None

    def __repr__(self):
        return f"{self.value}"