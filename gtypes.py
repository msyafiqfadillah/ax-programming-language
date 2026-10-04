class Type:
    def __init__(self, typeName):
        self.typeName = typeName

    def is_assignable(self, other):
        return (self == other
            or isinstance(other, EmptyType)
            or isinstance(other, AnyType))

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return self.typeName

class NumberType(Type):
    def __init__(self):
        super().__init__("number")

class StringType(Type):
    def __init__(self):
        super().__init__("string")

class BooleanType(Type):
    def __init__(self):
        super().__init__("boolean")

class EmptyType(Type):
    def __init__(self):
        super().__init__("empty")

    def is_assignable(self, other):
        return isinstance(other, Type)

class ListType(Type):
    def __init__(self, type):
        super().__init__(f"list[{type}]")

        self.type = type

    def is_assignable(self, other):
        if (isinstance(self, ListType) and isinstance(other, ListType)):
            return self.type.is_assignable(other.type)
        else:
            return (isinstance(other, (EmptyType, AnyType)))

    def __eq__(self, other):
        return isinstance(other, ListType) and (self.type == other.type)

    def __hash__(self):
        return hash(self.typeName)

# key type always String
class HashmapType(Type):
    def __init__(self, type):
        super().__init__(f"hashmap[{type}]")

        self.type = type

    def is_assignable(self, other):
        if (isinstance(self, HashmapType) and isinstance(other, HashmapType)):
            return self.type.is_assignable(other.type)
        else:
            return (isinstance(other, (EmptyType, AnyType)))

    def __eq__(self, other):
        return isinstance(other, HashmapType) and (self.type == other.type)

    def __hash__(self):
        return hash(self.typeName)

class FunctionType(Type):
    def __init__(self, param_types, return_type):
        params = ", ".join([str(t) for t in param_types])

        super().__init__(f"prc({params}) -> {return_type}")

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
            return (isinstance(other, (EmptyType, AnyType)))

    def __eq__(self, other):
        return (isinstance(other, FunctionType)
            and self.param_types == other.param_types
            and self.return_type == other.return_type)

class AnyType(Type):
    def __init__(self):
        super().__init__("any")

    def is_assignable(self, other):
        return True


def unify_types(types):
    if (not types):
        return AnyType()

    first = types[0]

    if (all(t == first for t in types)):
        return first

    if (all(isinstance(t, ListType) for t in types)):
        return ListType(unify_types([t.type for t in types]))

    if (all(isinstance(t, HashmapType) for t in types)):
        return HashmapType(unify_types([t.type for t in types]))

    return AnyType()


if (__name__ == "__main__"):
    x = FunctionType([ ListType(NumberType()) ], NumberType())
    y = FunctionType([ ListType(NumberType()), NumberType() ], NumberType())

    print(x.is_assignable(y))
