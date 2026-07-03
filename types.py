class Type:
    def is_assignable(self, other):
        return self == other or isinstance(other, EmptyType)

class NumberType(Type):
    def __eq__(self, other):
        return isinstance(other, NumberType)

    def __repr__(self):
        return "number"

class StringType(Type):
    def __eq__(self, other):
        return isinstance(other, StringType)

    def __repr__(self):
        return "string"

class BooleanType(Type):
    def __eq__(self, other):
        return isinstance(other, BooleanType)
    
    def __repr__(self):
        return "boolean"

class EmptyType(Type):
    def __eq__(self, other):
        return isinstance(other, EmptyType)
    
    def __repr__(self):
        return "empty"

class ListType(Type):
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, ListType) and (self.type == other.type)    

    def __repr__(self):
        return f"list[{self.type}]"

# key type always String
class HashmapType(Type):
    def __init__(self, value_type):
        self.value_type = value_type

    def __eq__(self, other):
        return isinstance(other, HashmapType) and (self.value_type == other.value_type)

    def __repr__(self):
        return f"hashmap[{StringType()}:{self.value_type}]"

class FunctionType(Type):
    def __init__(self, param_types, return_type):
        self.param_types = param_types
        self.return_type = return_type

    def __eq__(self, other):
        return (isinstance(other, FunctionType) 
            and self.param_types == other.param_types
            and self.return_type == other.return_type)

    def __repr__(self):
        params = ", ".join([str(t) for t in self.param_types])

        return f"prc({params}) -> {self.return_type}"
    