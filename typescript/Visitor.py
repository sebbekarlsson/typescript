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

    return update_requirements(
        visitor, _map[function_name]
        if function_name in _map else function_name
    )


def remap_type(ast_type):
    classname = ast_type.__class__.__name__
    if classname == 'ASTListType':
        if ast_type.data_type.__class__.__name__ == 'ASTStringType':
            return 'char**'

    if classname == 'ASTStringType':
        return 'char*'

    if classname == 'ASTNumberType':
        return 'int'

    if classname == 'ASTObjectInit':
        return ast_type.class_name + '*'

    return 'void'


def set_parent(child, parent):
    setattr(child, 'parent', parent)
    return child


jinja_env.globals.update(
    remap_type=remap_type,
    isinstance=isinstance,
    str=str
)


class Visitor(object):

    def __init__(self):
        self.requirements = []
        self.bootstraps = {}

    def transpile(self, tree):
        transpiled_code = self.visit(tree)

        if 'console.c' in self.bootstraps.keys():
            if '<stdlib.h>' not in self.requirements:
                self.requirements.append('<stdlib.h>')
            if '<stdio.h>' not in self.requirements:
                self.requirements.append('<stdio.h>')

        req = ''
        for requirement in self.requirements:
            req += '#include {}\n'.format(requirement)

        for k, v in self.bootstraps.items():
            req += v + '\n'

        if self.bootstraps:
            req += open('typescript/cbootstrap/bootstrap_init.c').read() + '\n'

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

    def visit_astarray(self, ast_node):
        template = jinja_env.get_template('array.c')

        return template.render(
            items=[self.visit(item) for item in ast_node.items]
        )

    def visit_astif(self, ast_node):
        template = jinja_env.get_template('if.c')
        expr = self.visit(ast_node.expr)
        body = self.visit(ast_node.statementlist)

        otherwise = self.visit(ast_node.otherwise)\
            if ast_node.otherwise else None

        return template.render(expr=expr, body=body, otherwise=otherwise)

    def visit_astwhile(self, ast_node):
        template = jinja_env.get_template('while.c')
        expr = self.visit(ast_node.expr)
        body = self.visit(ast_node.body)

        return template.render(expr=expr, body=body)

    def visit_astobjectinit(self, ast_node):
        template = jinja_env.get_template('struct_init.c')

        backref = None

        ast_node.args = [self.visit(a) for a in ast_node.args]

        if hasattr(ast_node, 'backref'):
            backref = ast_node.backref

        return template.render(
            object_init=ast_node,
            backref=backref
        )

    def visit_astdefinition(self, ast_node):
        template = jinja_env.get_template('definition.c')

        render_data_type = True

        if ast_node.value.__class__.__name__ == 'ASTObjectInit':
            ast_node.data_type = ast_node.value
            ast_node.value.backref = ast_node

        ast_node.value = self.visit(ast_node.value)

        if not isinstance(ast_node.key, basestring):
            render_data_type = False
            ast_node.key = self.visit(ast_node.key)

        return template.render(
            definition=ast_node, render_data_type=render_data_type)

    def visit_astclassdefinition(self, ast_node):
        template = jinja_env.get_template('struct_definition.c')

        update_requirements(self, 'class')

        return template.render(
            struct_name=ast_node.class_name,
            definitions=[
                self.visit(set_parent(d, ast_node))
                for d in ast_node.definitions
            ],
            allocations=ast_node.definitions,
            constructor_args=ast_node.constructor_args
        )

    def visit_astfunctiondefinition(self, ast_node):
        template = jinja_env.get_template('function_definition.c')

        ast_node.function_body = self.visit(ast_node.statements)
        ast_node.args = [self.visit(a) for a in ast_node.args]
        ast_node.args_visited = True

        if hasattr(ast_node, 'parent'):
            if ast_node.function_name == 'constructor':
                ast_node.parent.constructor_args = ast_node.args

        return template.render(definition=ast_node)

    def visit_astfunctioncall(self, ast_node):
        visited_args = [self.visit(arg) for arg in ast_node.args]

        backref = None

        template = Template(
            open('typescript/ctemplates/function_call.c').read())

        if hasattr(ast_node, 'backref'):
            backref = self.visit(ast_node.backref)

        return template.render(
            function_name=remap_function(self, ast_node.function_name),
            backref=backref,
            args=visited_args
        )

    def visit_astvariable(self, ast_node):
        return ast_node.key

    def visit_nonetype(self, ast_node):
        return None

    def visit_astthis(self, ast_node):
        return 'self'

    def visit_astattributeaccess(self, ast_node):
        ast_node.ast_node.backref = ast_node.key
        key = self.visit(ast_node.key)

        if key == 'console':
            if 'console.c' not in self.bootstraps:
                self.bootstraps['console.c'] =\
                    open('typescript/cbootstrap/console.c').read()

        child = self.visit(ast_node.ast_node)

        template = jinja_env.get_template('attribute_access.c')

        return template.render(key=key, child=child)

    def visit_astinterface(self, ast_node):
        template = jinja_env.get_template('interface.c')

        return template.render(
            interface_name=ast_node.interface_name,
            definitions=[self.visit(d) for d in ast_node.definition_list]
        )

    def visit_astbinop(self, ast_node):
        template = jinja_env.get_template('binop.c')

        operator = self.visit(ast_node.operator)
        left = self.visit(ast_node.left)
        right = self.visit(ast_node.right)

        return template.render(operator=operator, left=left, right=right)

    def visit_token(self, token):
        return token.value
