from typescript.Lexer import Lexer
from typescript.Parser import Parser
from typescript.Visitor import Visitor

import sys

import subprocess


def run():
    contents = open(sys.argv[1]).read()
    lexer = Lexer(contents)
    parser = Parser(lexer)
    tree = parser.parse()
    visitor = Visitor()
    code = visitor.transpile(tree)

    open('main.c', 'w+').write(code)
    indent_process = subprocess.Popen(
        ['indent', 'main.c'], stdout=subprocess.PIPE)
    indent_process.communicate()
