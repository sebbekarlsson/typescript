class ASTFunctionDefinition(object):

    def __init__(self, data_type, function_name, args, statements):
        self.data_type = data_type
        self.function_name = function_name
        self.args = args
        self.statements = statements
