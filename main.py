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

    prc hxh(name: string, age: number): any {
        if (name == "gon") {
            return name
        } whatever {
            return age
        }
    }

    show(hxh("gon", 123))
    show(type(hxh))
"""

main(source)
