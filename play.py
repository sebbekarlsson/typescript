from typescript.Lexer import Lexer
from typescript.TokenType import TokenType
from typescript.Parser import Parser
from typescript.Visitor import Visitor


contents = open('examples/main.ts').read()
lexer = Lexer(contents)
parser = Parser(lexer)
tree = parser.parse()
visitor = Visitor()
visitor.visit(tree)
