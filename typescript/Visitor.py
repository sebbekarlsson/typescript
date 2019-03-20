class Visitor(object):

    def visit(self, ast_node):
        return getattr(
            self,
            'visit_' + str(ast_node.__class__.__name__.lower())
        )(ast_node)

    def visit_aststatementlist(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visit_astdefinition(self, ast_node):
        return None

    def visit_astfunctiondefinition(self, ast_node):
        return None

    def visit_astfunctioncall(self, ast_node):
        visited_args = [self.visit(arg) for arg in ast_node.args]
        return visited_args

    def visit_astvariable(self, ast_node):
        return ast_node.key

    def visit_nonetype(self, ast_node):
        return None
