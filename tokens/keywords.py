class Keywords:
    VAR = "var"
    SET = "set"
    FCT = "fct"
    LOOP = "loop"
    RETURN = "return"
    IF = "if"
    MAYBE = "maybe"
    ELSE = "else"

    @classmethod
    def all(cls):
        return {
            cls.VAR,
            cls.SET,
            cls.FCT,
            cls.LOOP,
            cls.RETURN,
            cls.IF,
            cls.MAYBE,
            cls.ELSE
        }
