# -*- coding:utf-8 -*-

import os

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
            if static_info.endswith(".jpg"):
                content_type = 'image/jpg'
            elif static_info.endswith(".gif"):
                content_type = 'image/gif'
            elif static_info.endswith(".ico"):
                content_type = 'image/x-icon'
            elif static_info.endswith(".js"):
                content_type = 'application/javascript'
            elif static_info.endswith(".css"):
                content_type = 'text/css'
            print static_info, content_type
            if content_type:
                with open(static_info) as f:
                    output = f.read()
                    status = "200 OK"
        except IOError:
            pass
        response_headers = [('Content-Type', content_type or "text/html"),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
