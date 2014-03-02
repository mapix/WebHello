# -*- coding:utf-8 -*-

import os
from mimetypes import guess_type

__all__ = ["Static"]


class Static(object):

    def __init__(self, application, static_config, rewrite_rule=None):
        self.application = application
        self.url_prefix, self.dictory_prefix = static_config
        self.rewrite_rule = rewrite_rule

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO')
        if self.rewrite_rule and path_info in self.rewrite_rule:
            path_info = environ['PATH_INFO'] = self.rewrite_rule[path_info]
        if path_info.startswith(self.url_prefix):
            return self.serve_static(environ, start_response)
        return self.application(environ, start_response)

    def serve_static(self, environ, start_response):
        status = "404 Not Found"
        content_type = None
        static_info = os.path.join(self.dictory_prefix,
                                   environ.get('PATH_INFO')[len(self.url_prefix):])
        output = "404 Not Found"
        try:
            mime_type = guess_type(static_info)
            if mime_type:
                with open(static_info) as f:
                    output = f.read()
                    status, content_type = "200 OK", mime_type[0]
        except IOError:
            pass
        response_headers = [('Content-Type', content_type or "text/html"),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
