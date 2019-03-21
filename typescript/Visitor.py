from jinja2 import Template, Environment, PackageLoader


jinja_env = Environment(loader=PackageLoader('typescript', 'ctemplates'))


def update_requirements(visitor, keyword):
    _map = {
        'printf': '<stdio.h>',
        'class': '<stdlib.h>'
    }

    requirement = _map[keyword] if keyword in _map else None

    if requirement not in visitor.requirements and requirement:
        visitor.requirements.append(requirement)

    return keyword


def remap_function(visitor, function_name):
    _map = {
        'print': 'printf'
    }

    return update_requirements(visitor, _map[function_name] if function_name in _map else function_name)


def remap_type(ast_type):
    classname = ast_type.__class__.__name__
    if classname == 'ASTListType':
        if ast_type.data_type.__class__.__name__ == 'ASTStringType':
            return 'char**'

    if classname == 'ASTStringType':
        return 'char*'

    if classname == 'ASTNumberType':
        return 'int'

    return 'void'


jinja_env.globals.update(
    remap_type=remap_type
)




class Visitor(object):

    def __init__(self):
        self.requirements = []

    def transpile(self, tree):
        transpiled_code = self.visit(tree)
        req = ''
        for requirement in self.requirements:
            req += '#include {}\n'.format(requirement)

        return req + '\n\n' + transpiled_code

    def visit(self, ast_node):
        return getattr(
            self,
            'visit_' + str(ast_node.__class__.__name__.lower())
        )(ast_node)

    def visit_aststatementlist(self, ast_node):
        out = ''
        for statement in ast_node.statements:
            _out = self.visit(statement)

            if _out:
                out += _out + ';\n'

        return out

    def visit_str(self, ast_node):
        return '"' + ast_node + '"'

    def visit_astdefinition(self, ast_node):
        template = jinja_env.get_template('definition.c')

        ast_node.value = self.visit(ast_node.value)

        return template.render(definition=ast_node)

    def visit_astclassdefinition(self, ast_node):
        template = jinja_env.get_template('struct_definition.c')

        update_requirements(self, 'class')

        return template.render(
            struct_name=ast_node.class_name,
            definitions=ast_node.definitions
        )

    def visit_astfunctiondefinition(self, ast_node):
        visited_args = [self.visit(arg) for arg in ast_node.args]

        template = Template(
            open('typescript/ctemplates/function_definition.c').read())

        return template.render(
            data_type='int' if ast_node.data_type.__class__.__name__ ==
            'ASTNumberType' else None,
            function_name=ast_node.function_name,
            args=visited_args,
            function_body=self.visit(ast_node.statements)
        )


    def visit_astfunctioncall(self, ast_node):
        visited_args = [self.visit(arg) for arg in ast_node.args]

        template = Template(
            open('typescript/ctemplates/function_call.c').read())

        return template.render(
            function_name=remap_function(self, ast_node.function_name),
            args=visited_args
        )

    def visit_astvariable(self, ast_node):
        return ast_node.key

    def visit_nonetype(self, ast_node):
        return None
