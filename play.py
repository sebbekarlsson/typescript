from typescript.Lexer import Lexer
from typescript.TokenType import TokenType
from typescript.Parser import Parser


contents = open('examples/variables.ts').read()
lexer = Lexer(contents)
parser = Parser(lexer)
parser.parse()
