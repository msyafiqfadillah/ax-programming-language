class Keywords:
    VAR = "var"
    SET = "set"
    PRC = "prc"
    LOOP = "loop"
    RETURN = "return"
    IF = "if"
    MAYBE = "maybe"
    WHATEVER = "whatever"
    TRUE = "true"
    FALSE = "false"
    EMPTY = "empty"
    UNDEFINED = "undefined"
    CONTINUE = "continue"

    @classmethod
    def all(cls):
        return {
            cls.VAR,
            cls.SET,
            cls.PRC,
            cls.LOOP,
            cls.RETURN,
            cls.IF,
            cls.MAYBE,
            cls.WHATEVER,
            cls.TRUE,
            cls.FALSE,
            cls.EMPTY,
            cls.UNDEFINED,
            cls.CONTINUE
        }
