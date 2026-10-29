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
    var x: boolean = true
    var inc: number = 0

    loop (x) {
        if (inc == 6) {
            set x = false
        } maybe (inc == 3) {
            set inc += 1

            continue
        }

        show(inc)

        set inc += 1
    }

    show(inc)
"""

main(source)
