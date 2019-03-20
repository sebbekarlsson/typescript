class ASTFunctionDefinition(object):

    def __init__(self, function_name, args, statements):
        self.function_name = function_name
        self.args = args
        self.statements = statements
