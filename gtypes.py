class Type:
    def is_assignable(self, other):
        return (self == other 
            or isinstance(other, EmptyType) 
            or isinstance(other, AnyType))

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

    def is_assignable(self, other):
        if (isinstance(self, ListType) and isinstance(other, ListType)):
            return self.type.is_assignable(other.type)
        else:
            if (isinstance(other, (EmptyType, AnyType))):
                return True

            return False
            
    def __eq__(self, other):
        return isinstance(other, ListType) and (self.type == other.type)    

    def __repr__(self):
        return f"list[{self.type}]"

# key type always String
class HashmapType(Type):
    def __init__(self, type):
        self.type = type

    def is_assignable(self, other):
        if (isinstance(self, HashmapType) and isinstance(other, HashmapType)):
            return self.type.is_assignable(other.type)
        else:
            if (isinstance(other, (EmptyType, AnyType))):
                return True

            return False

    def __eq__(self, other):
        return isinstance(other, HashmapType) and (self.type == other.type)

    def __repr__(self):
        return f"hashmap[{self.type}]"

class FunctionType(Type):
    def __init__(self, param_types, return_type):
        self.param_types = param_types
        self.return_type = return_type

    def __is_assignable_params(self, other):
        index = 0
        lspt = len(self.param_types)
        lopt = len(other.param_types)

        if (lspt != lopt):
            return False

        trigger = lspt

        while (index < trigger):
            if (not self.param_types[index].is_assignable(other.param_types[index])):
                return False

            index += 1

        return True

    def __is_assignable_return(self, other):
        return self.return_type.is_assignable(other.return_type)

    def is_assignable(self, other):
        if (isinstance(self, FunctionType) and isinstance(other, FunctionType)):
            is_param_same = self.__is_assignable_params(other)
            is_return_same = self.__is_assignable_return(other)
            act_result = is_param_same and is_return_same

            return act_result
        else:
            if (isinstance(other, (EmptyType, AnyType))):
                return True

            return False

    def __eq__(self, other):
        return (isinstance(other, FunctionType) 
            and self.param_types == other.param_types
            and self.return_type == other.return_type)

    def __repr__(self):
        params = ", ".join([str(t) for t in self.param_types])

        return f"prc({params}) -> {self.return_type}"

class AnyType(Type):
    def __eq__(self, other):
        return isinstance(other, AnyType)

    def is_assignable(self, other):
        return True

    def __repr__(self):
        return "any"


if (__name__ == "__main__"):
    x = FunctionType([ ListType(NumberType()) ], NumberType())
    y = FunctionType([ ListType(NumberType()), NumberType() ], NumberType())

    print(x.is_assignable(y))