from collections import namedtuple


token_map = {
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}',
    'SEMI': ';',
    'COLON': ':',
    'THIS': 'this',
    'NEW': 'new',
    'DOT': '.',
    'RETURN': 'return',
    'IF': 'if',
    'ELSE': 'else',
    'WHILE': 'while',
    'FOR': 'for',
    'LET': 'let',
    'NUMBER': 'number',
    'BOOLEAN': 'boolean',
    'STRING': 'string',
    'VOID': 'void',
    'NULL': 'null',
    'ANY': 'any',
    'FALSE': 'false',
    'TRUE': 'true',
    'FUNCTION': 'function',
    'EOF': '\0',
    'ID': 'ID',
    'EQUALS': '=',
    "QUOTE": '"'
}


_TokenType = namedtuple('TokenType', ' '.join(token_map.keys()))
TokenType = _TokenType(**token_map)


def token_type_by_value(value):
    for k, v in token_map.items():
        if v == value:
            return k
