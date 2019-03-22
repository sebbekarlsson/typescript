from collections import namedtuple


token_map = {
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'SEMI': ';',
    'COLON': ':',
    'COMMA': ',',
    'THIS': 'this',
    'NEW': 'new',
    'DOT': '.',
    'RETURN': 'return',
    'IF': 'if',
    'ELSE': 'else',
    'WHILE': 'while',
    'FOR': 'for',
    'LET': 'let',
    'NUMBER_TYPE': 'number',
    'BOOLEAN_TYPE': 'boolean',
    'STRING_TYPE': 'string',
    'STRING_VALUE': 'STRING_VALUE',
    'VOID_TYPE': 'void',
    'NULL_TYPE': 'null',
    'ANY_TYPE': 'any',
    'FALSE_VALUE': 'false',
    'TRUE_VALUE': 'true',
    'FUNCTION_TYPE': 'function',
    'EOF': '\0',
    'ID': 'ID',
    'EQUALS': '=',
    'QUOTE': '"',
    'CLASS_TYPE': 'class',
    'INTERFACE_TYPE': 'interface',
    'PLUS': '+',
    'SUBTRACT': '-',
    'MULTIPLY': '*',
    'DIVIDE': '/'
}


_TokenType = namedtuple('TokenType', ' '.join(token_map.keys()))
TokenType = _TokenType(**{k: k for k, v in token_map.items()})


def token_type_by_value(value):
    for k, v in token_map.items():
        if v == value:
            return k
