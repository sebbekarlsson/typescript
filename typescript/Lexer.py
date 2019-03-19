from typescript.TokenType import token_map, token_type_by_value, TokenType
from typescript.Token import Token
from typescript.exceptions import UnexpectedToken


class Lexer(object):

    def __init__(self, contents):
        self.contents = contents
        self.pointer = 0
        self.current_char = self.contents[self.pointer]

    def ok(self):
        return self.pointer < len(self.contents) - 1

    def should_skip_whitespace(self):
        return self.current_char == ' ' or ord(self.current_char) == 10

    def advance(self):
        if self.ok():
            self.pointer += 1
            self.current_char = self.contents[self.pointer]
        else:
            self.current_char = '\0'

    def skip_whitespace(self):
        while self.should_skip_whitespace():
            self.advance()

    def parse_id(self):
        _id = ''
        while self.current_char.isalnum():
            _id += self.current_char
            self.advance()

        if _id in token_map.values():
            return Token(token_type_by_value(_id), _id)
        else:
            return Token(TokenType.ID, _id)

    def get_next_token(self):
        while self.ok():
            if self.should_skip_whitespace():
                self.skip_whitespace()

            if self.current_char.isalnum():
                return self.parse_id()

            if self.current_char in token_map.values():
                token = Token(
                    token_type_by_value(self.current_char),
                    self.current_char
                )
                self.advance()
                return token

            raise UnexpectedToken(self.current_char)

        return Token(TokenType.EOF, '\0')
