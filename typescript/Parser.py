from typescript.exceptions import UnexpectedToken
from typescript.TokenType import TokenType
from typescript.ast.ASTDefinition import ASTDefinition
from typescript.ast.ASTStatementList import ASTStatementList
from typescript.ast.ASTFunctionCall import ASTFunctionCall
from typescript.ast.ASTVariable import ASTVariable
from typescript.ast.ASTListType import ASTListType
from typescript.ast.ASTFunctionDefinition import ASTFunctionDefinition
from typescript.ast.ASTNumberType import ASTNumberType
from typescript.ast.ASTStringType import ASTStringType
from typescript.ast.ASTClassDefinition import ASTClassDefinition
from typescript.ast.ASTObjectInit import ASTObjectInit
from typescript.ast.ASTAttributeAccess import ASTAttributeAccess
from typescript.ast.ASTThis import ASTThis


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
            raise UnexpectedToken(
                'expected {} but got {}'.format(
                    token_type,
                    self.current_token.__dict__
                )
            )
        else:
            self.current_token = self.lexer.get_next_token()

    def parse_expr(self):
        return self.parse_statement()

    def parse_string_value(self):
        value = self.current_token.value
        self.eat(TokenType.STRING_VALUE)
        return value

    def parse_eof(self):
        return None

    def parse_attribute_access(self, id_token):
        self.eat(TokenType.DOT)
        access = ASTAttributeAccess(id_token, self.parse_id())

        if self.current_token.token_type == TokenType.EQUALS:
            return self.parse_definition(key=access)

        return access

    def parse_this(self):
        self.eat(TokenType.THIS)
        return self.parse_attribute_access(ASTThis())

    def parse_object_init(self):
        self.eat(TokenType.NEW)
        id_token = self.current_token
        self.eat(TokenType.ID)

        self.eat(TokenType.LPAREN)
        args = []

        expr = self.parse_expr()\
            if self.current_token.token_type != TokenType.RPAREN else None

        if expr:
            args.append(expr)

        while self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            expr = self.parse_expr()

            expr = self.parse_expr()\
                if self.current_token.token_type != TokenType.RPAREN else None

            if expr:
                args.append(expr)

        self.eat(TokenType.RPAREN)

        return ASTObjectInit(id_token.value, args)

    def parse_new(self):
        return self.parse_object_init()

    def parse_function_call(self, id_token):
        function_name = id_token.value
        self.eat(TokenType.LPAREN)
        args = []

        expr = self.parse_expr()\
            if self.current_token.token_type != TokenType.RPAREN else None

        if expr:
            args.append(expr)

        while self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            expr = self.parse_expr()

            expr = self.parse_expr()\
                if self.current_token.token_type != TokenType.RPAREN else None

            if expr:
                args.append(expr)

        self.eat(TokenType.RPAREN)

        return ASTFunctionCall(function_name, args)

    def parse_function_definition(self):
        data_type = None
        function_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        args = []

        definition = self.parse_definition()\
            if self.current_token.token_type == TokenType.ID else None

        if definition:
            args.append(definition)

        while self.current_token.token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA)

            definition = self.parse_definition()\
                if self.current_token.token_type == TokenType.ID else None

            if definition:
                args.append(definition)

        self.eat(TokenType.RPAREN)

        if self.current_token.token_type == TokenType.COLON:
            self.eat(TokenType.COLON)
            data_type = self.parse_data_type()

        self.eat(TokenType.LBRACE)
        statements = self.parse_statement_list()
        self.eat(TokenType.RBRACE)

        return ASTFunctionDefinition(data_type, function_name, args, statements)

    def parse_function_type(self):
        self.eat(TokenType.FUNCTION_TYPE)
        return self.parse_function_definition()

    def parse_definition_list(self):
        definitions = []

        if self.current_token.token_type == TokenType.FUNCTION_TYPE:
            self.eat(TokenType.FUNCTION_TYPE)
            definition = self.parse_function_definition()
        else:
            definition = self.parse_definition()

        if definition:
            definitions.append(definition)

        while self.current_token.token_type == TokenType.SEMI:
            self.eat(TokenType.SEMI)

            if self.current_token.token_type == TokenType.FUNCTION_TYPE:
                self.eat(TokenType.FUNCTION_TYPE)
                definition = self.parse_function_definition()
            else:
                definition = self.parse_definition() if\
                    self.current_token.token_type != TokenType.RBRACE else None

            if definition:
                definitions.append(definition)

        return definitions

    def parse_class_definition(self):
        class_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LBRACE)
        definitions = self.parse_definition_list()
        self.eat(TokenType.RBRACE)

        return ASTClassDefinition(class_name, definitions)

    def parse_class_type(self):
        self.eat(TokenType.CLASS_TYPE)
        return self.parse_class_definition()

    def parse_variable(self, id_token):
        return ASTVariable(id_token.value)

    def parse_number_type(self):
        self.eat(TokenType.NUMBER_TYPE)
        return self.current_token

    def parse_string_type(self):
        self.eat(TokenType.STRING_TYPE)
        return self.current_token

    def parse_list_type(self, data_type):
        self.eat(TokenType.LBRACKET)
        self.eat(TokenType.RBRACKET)
        return ASTListType(data_type)

    def parse_data_type(self):
        data_type = self.current_token
        self.eat(data_type.token_type)

        if data_type.token_type == TokenType.NUMBER_TYPE:
            data_type = ASTNumberType(data_type)
        elif data_type.token_type == TokenType.STRING_TYPE:
            data_type = ASTStringType(data_type)

        if self.current_token.token_type == TokenType.LBRACKET:
            return self.parse_list_type(data_type)

        return data_type

    def parse_id(self):
        if self.current_token.token_type == TokenType.ID:
            id_token = self.current_token
            self.eat(TokenType.ID)
        else:
            return self.parse_data_type()

        if self.current_token.token_type == TokenType.LPAREN:
            return self.parse_function_call(id_token)

        if self.current_token.token_type == TokenType.COLON:
            return self.parse_definition(key=id_token.value)

        node = self.parse_variable(id_token)

        if self.current_token.token_type == TokenType.DOT:
            return self.parse_attribute_access(node)

        return node

    def parse_definition(self, key=None):
        expr = None
        data_type = None

        if self.current_token.token_type == TokenType.LET:
            self.eat(TokenType.LET)

        if not key:
            key = self.current_token.value
            self.eat(TokenType.ID)

        if self.current_token.token_type == TokenType.COLON:
            self.eat(TokenType.COLON)
            data_type = self.parse_id()

        if (self.current_token.token_type == TokenType.EQUALS):
            self.eat(TokenType.EQUALS)
            expr = self.parse_expr()

        return ASTDefinition(data_type=data_type, key=key, value=expr)

    def parse_statement(self):
        if self.current_token.token_type in [
            TokenType.LBRACE,
            TokenType.RBRACE,
            TokenType.LBRACKET,
            TokenType.RBRACKET
        ]:
            return

        return getattr(
            self,
            get_method(self.current_token.token_type)
        )()

    def parse_statement_list(self):
        statements = []

        statement = self.parse_statement()

        if statement:
            statements.append(statement)

        while self.current_token.token_type == TokenType.SEMI:
            self.eat(TokenType.SEMI)

            statement = self.parse_statement()

            if statement:
                statements.append(statement)

        return ASTStatementList(statements)
