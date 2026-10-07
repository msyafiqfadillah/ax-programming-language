class Types:
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    EMPTY = "empty"
    LIST = "list"
    HASHMAP = "hashmap"
    ANY = "any"

    @classmethod
    def all(cls):
        return [
            cls.NUMBER,
            cls.STRING,
            cls.BOOLEAN,
            cls.EMPTY,
            cls.LIST,
            cls.HASHMAP,
            cls.ANY,
        ]
