import re
from tokens.keywords import Keywords
from tokens.punctuations import Punctuations 
from tokens.operators import Operators


class Scanner:
    def __init__(self):
        self.c_index = 0
        self.token_streams = []

    def add_token(self, type, value):
        n_token = { "type": type, "value": value }

        self.token_streams.append(n_token)

    def is_eof(self):
        return self.c_index >= len(self.raw_source)

    def peek(self):
        if (self.is_eof()):
            raise TypeError("Unterminated string literal")
        
        return self.raw_source[self.c_index]

    def advance(self):
        c_char = self.peek()

        self.c_index += 1

        return c_char
    
    def stream_scan(self, first_char, allowed):
        result = first_char

        while (not self.is_eof() and re.match(allowed, self.peek())):
            result += self.advance()

        return result
    
    def string_scan(self, quote):
        result = ""

        while (not self.is_eof() and self.peek() != quote):
            result += self.advance()

        self.advance()

        return result

    def scans(self, raw_source):
        self.raw_source = raw_source

        while (not self.is_eof()):
            c_char = self.advance()

            if (c_char.isspace()):
                continue

            if (c_char == Punctuations.FLAG):
                while (not self.is_eof() and self.peek() != Punctuations.FLAG):
                    self.advance()

                if (self.is_eof()):
                    raise TypeError("Missing closing FLAG '~'")

                self.advance()

                continue

            if (c_char == Punctuations.HASHTAG):
                while (self.advance() != "\n"):
                    continue
                continue

            # OPERATOR
            if (c_char == Operators.EQUAL):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.D_EQUAL)
                    self.advance()
                    continue

                self.add_token("OPERATOR", Operators.EQUAL)
            
            elif (c_char == Operators.NEGATION):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.N_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.NEGATION)

            elif (c_char == Operators.GREATER):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.G_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.GREATER)

            elif (c_char == Operators.LESS):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.L_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.LESS)
            
            elif (c_char == Operators.ADDITION):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.A_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.ADDITION)

            elif (c_char == Operators.SUBTRACTION):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.S_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.SUBTRACTION)

            elif (c_char == Operators.MULTIPLICATION):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.M_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.MULTIPLICATION)
            
            elif (c_char == Operators.DIVISION):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.D_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.DIVISION)

            elif (c_char == Operators.MODULO):
                if (self.peek() == Operators.EQUAL):
                    self.add_token("OPERATOR", Operators.MO_EQUAL)
                    self.advance()
                    continue
                
                self.add_token("OPERATOR", Operators.MODULO)
            
            elif (c_char == Operators.POWER):
                self.add_token("OPERATOR", Operators.POWER)

            elif (c_char == "|" and self.peek() == "|"):
                self.add_token("OPERATOR", Operators.OR)
                self.advance()

            elif (c_char == "&" and self.peek() == "&"):
                self.add_token("OPERATOR", Operators.AND)
                self.advance()

            # NUMBER
            elif (re.match("[.0-9]", c_char)):
                rs = self.stream_scan(c_char, "[.0-9]")
                self.add_token("NUMBER", rs)

            # STRING
            elif (c_char in ("'", '"')):
                rs = self.string_scan(c_char)
                self.add_token("STRING", rs)

            elif (re.match("[_a-zA-Z0-9]", c_char)):
                rs = self.stream_scan(c_char, "[_a-zA-Z0-9]")

                if (rs in Keywords.all()): # KEYWORDS
                    self.add_token("KEYWORDS", rs)
                else:                      # IDENTIFIER
                    self.add_token("IDENTIFIER", rs)

            # PUNCTUATIONS
            elif (c_char in Punctuations.all()):
                self.add_token("PUNCTUATIONS", c_char)

            else:
                pass

        return self.token_streams


def main() :
    scanner = Scanner()

    # sample = '''
    #     prc foo(param_1, param_2) {
    #         var new_x = 12
    #         set new_x = 99
    #         set new_x = (new_x + 2) * 99
    #     }

    #     foo()
    # '''

    sample = '''
        var x = 2 * 2 ^ 2
        var z = 2 < 9
    '''

    tokens = scanner.scans(sample)

    print(tokens)


if __name__ == "__main__":
    main()
