from __future__ import unicode_literals
from jinja2 import Environment
from jinja2 import Template
from jinja2.ext import Extension
from jinja2.lexer import Token
from jinja2.utils import Markup

from threading import local
_thread_local = local()

class SqlExtension(Extension):
    def filter_stream(self, stream):
        """
        We convert 
        {{ some.variable | filter1 | filter 2}}
            to 
        {{ some.variable | filter1 | filter 2 | bind}}
        
        ... for all variable declarations in the template

        This function is called by jinja2 immediately 
        after the lexing stage, but before the parser is called. 
        """
        while not stream.eos:
            token = next(stream)
            if token.test("variable_begin"):
                var_expr = []
                while not token.test("variable_end"):
                    var_expr.append(token)
                    token = next(stream)
                variable_end = token

                last_token = var_expr[-1]
                if (not last_token.test("name") 
                    or not last_token.value in ('bind', 'inclause', 'sqlsafe')):
                    # don't bind twice
                    var_expr.append(Token(10, 'pipe', u'|'))
                    var_expr.append(Token(10, 'name', u'bind'))

                var_expr.append(variable_end)

                for token in var_expr:
                    yield token
            else:
                yield token

def sql_safe(value):
    """Filter to mark the value of an expression as safe for inserting
    in a SQL statement"""
    return Markup(value)

def bind(value):
    """A filter that prints %s, and stores the value 
    in an array, so that it can be bound using a prepared statement

    This filter is automatically applied to every {{variable}} 
    during the lexing stage, so developers can't forget to bind
    """
    if isinstance(value, Markup):
        return value
    elif requires_in_clause(value):
        raise Exception("""Got a list or tuple. 
            Did you forget to apply '|inclause' to your query?""")
    else:
        _thread_local.bind_params.append(value)
    return "%s"

def bind_in_clause(value):
    values = list(value)
    clause = ",".join(['%s'] * len(values))
    clause = "(" + clause + ")"
    for v in values:
        _thread_local.bind_params.append(v)
    return clause

def requires_in_clause(obj):
    return hasattr(obj, '__iter__')

class JinjaSql(object):
    def __init__(self, env=None):
        self.env = env or Environment()
        self._prepare_environment()

    def _prepare_environment(self):
        self.env.autoescape=True
        self.env.add_extension(SqlExtension)
        self.env.add_extension('jinja2.ext.autoescape')
        self.env.filters["bind"] = bind
        self.env.filters["sqlsafe"] = sql_safe
        self.env.filters["inclause"] = bind_in_clause

    def prepare_query(self, source, data):
        template = self.env.from_string(source)
        return self._prepare_query(template, data)

    def _prepare_query(self, template, data):
        try:
            _thread_local.bind_params = []
            query = template.render(**data)
            bind_params = _thread_local.bind_params
            return query, bind_params
        finally:
            del _thread_local.bind_params
