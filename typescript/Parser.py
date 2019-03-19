from typescript.exceptions import UnexpectedToken
from typescript.TokenType import TokenType


def get_method(token_type):
    if token_type == 'LET':
        return 'parse_definition'

    return 'parse_' + token_type.lower()


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        return self.parse_statement_list()

    def eat(self, token_type):
        if not self.current_token.token_type == token_type:
            raise UnexpectedToken(self.current_token.value)
        else:
            self.current_token = self.lexer.get_next_token()

    def parse_expr(self):
        return None

    def parse_definition(self):
        if self.current_token.token_type == TokenType.LET:
            self.eat(TokenType.LET)

        self.eat(TokenType.ID)
        expr = self.parse_expr()

    def parse_statement(self):
        return getattr(
            self,
            get_method(self.current_token.token_type)
        )()

    def parse_statement_list(self):
        self.parse_statement()

        while self.current_token == TokenType.SEMI:
            self.parse_statement()
