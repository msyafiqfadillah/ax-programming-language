class Operators:
    EQUAL = "="
    G_EQUAL = ">="
    L_EQUAL = "<="
    D_EQUAL = "=="
    N_EQUAL = "!="
    A_EQUAL = "+="
    M_EQUAL = "*="
    S_EQUAL = "-="
    D_EQUAL = "/="
    P_EQUAL = "^="
    MO_EQUAL = "%="
    ADDITION = "+"
    MULTIPLICATION = "*"
    SUBTRACTION = "-"
    DIVISION = "/"
    POWER = "^"
    MODULO = "%"
    NEGATION = "!"
    GREATER = ">"
    LESS = "<"

    @classmethod
    def all(cls):
        return {
            cls.EQUAL,
            cls.G_EQUAL,
            cls.L_EQUAL,
            cls.D_EQUAL,
            cls.N_EQUAL,
            cls.A_EQUAL,
            cls.M_EQUAL,
            cls.S_EQUAL,
            cls.D_EQUAL,
            cls.P_EQUAL,
            cls.MO_EQUAL,
            cls.ADDITION,
            cls.MULTIPLICATION,
            cls.SUBTRACT,
            cls.DIVISION,
            cls.POWER,
            cls.MODULO,
            cls.NEGATION,
            cls.GREATER,
            cls.LESS
        }

