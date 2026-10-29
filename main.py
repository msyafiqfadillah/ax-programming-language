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
    var x: number = 123
    var y: number = 222

    if (x == y) {
        show(222)
    } maybe (x < y) {
        if (true) {
            show(7171)
        }

        show(888)
    } maybe (x != y) {
        show(999)
    } whatever {
        show("abc")
    }
"""

main(source)
