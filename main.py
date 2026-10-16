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
    var ggg: func(number) -> number = prc(z: number): number {
        return 1 + 2
    }
"""

main(source)
