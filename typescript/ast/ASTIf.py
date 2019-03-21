class ASTIf(object):

    def __init__(self, expr, otherwise, statementlist):
        self.expr = expr
        self.otherwise = otherwise
        self.statementlist = statementlist
