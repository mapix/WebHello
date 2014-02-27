# -*- coding:utf-8 -*-

import re
import sys

__all__ = ["Router"]

VAR_REGEX = re.compile(r'''
    \{          # The exact character "{"
    (?P<var>\w+)       # The variable name (restricted to a-z, 0-9, _)
    (?::(?P<regex>([^}]+)))? # The optional :regex part
    \}          # The exact character "}"
    ''', re.VERBOSE)


class Router(object):

    def __init__(self, routes=[]):
        self.routes = []
        for template, controller in routes:
            self.add_route(template, controller)

    def add_route(self, template, controller):
        if isinstance(controller, basestring):
            controller = _load_controller(controller)
        self.routes.append((re.compile(_template_to_regex(template)), controller))

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO')
        for regex, controller in self.routes:
            print path_info, regex.pattern, regex.match(path_info)
            match = regex.match(path_info)
            if match:
                urlvars = match.groupdict()
                output = controller(None, **urlvars)
                status = "200 OK"
                response_headers = [('Content-Type', 'text/html'),
                                    ('Content-Length', str(len(output)))]
                start_response(status, response_headers)
                return [output]
        raise Exception('404')


def _template_to_regex(template):
    regex, last_pos = '', 0
    for match in VAR_REGEX.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        regex += '(?P<%s>%s)' % (match.group('var'), match.group('regex') or '[^/]+')
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    return '^%s$' % regex


def _load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    return getattr(module, func_name)
