# -*- coding:utf-8 -*-

import re
import sys

from .request import Request
from .response import Response
from .exception import HTTPException, HTTPNotFound

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
        self.routes.append((re.compile(_template_to_regex(template)),
                            controller))

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.try_publish(request)
        return response(environ, start_response)

    def try_publish(self, request):
        path_info = request.get_path_info()
        try:
            for regex, controller in self.routes:
                match = regex.match(path_info)
                if match:
                    urlvars = match.groupdict()
                    return Response(controller(request, **urlvars), request=request)
            raise HTTPNotFound("request %r not found" % path_info)
        except HTTPException as http_error:
            http_error.request = request
            return http_error
        except:
            raise


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
