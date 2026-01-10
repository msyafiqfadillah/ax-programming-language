class Keywords:
    VAR = "var"
    SET = "set"
    PRC = "prc"
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
            cls.PRC,
            cls.LOOP,
            cls.RETURN,
            cls.IF,
            cls.MAYBE,
            cls.ELSE
        }
