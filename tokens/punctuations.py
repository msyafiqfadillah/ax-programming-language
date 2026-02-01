class Punctuations:
    PARANTHESSES_O = "("
    PARANTHESSES_C = ")"
    CURVED_O = "{"
    CURVED_C =  "}"
    SQUARE_O = "["
    SQUARE_C = "]"
    V_LINE = "|"
    COLON = ":"
    COMMA = ","

    @classmethod
    def all(cls):
        return {
            cls.PARANTHESSES_O,
            cls.PARANTHESSES_C,
            cls.CURVED_O,
            cls.CURVED_C,
            cls.SQUARE_O,
            cls.SQUARE_C,
            cls.V_LINE,
            cls.COLON,
            cls.COMMA
        }

