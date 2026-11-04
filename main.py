from scanner import Scanner
from parser import Parser
from type_checker import TypeChecker
from interpreter import Interpreter

def main(source):
    tokens = Scanner().scans(source)
    ast = Parser().parse_program(tokens)

    TypeChecker().check(ast)
    Interpreter().run(ast)

source = """
    var x: func(number) -> number = prc (h: number): number {
        return 2+h
    }
    var z: number = x(99)
    var funcs: list[func(number) -> number] = [
        prc(a: number): number { return a * 2 },
        prc(b: number): number { return b ^ 2 },
        prc(c: number): number { return c + 30 }
    ]
    var fc0: number = funcs[0](3)

    # show(fc0)

    var p: list[list[number]] = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    p[0][1]

    var hhh: number = 123
    hhh[0]
"""

main(source)
