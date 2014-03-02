# -*- coding:utf-8 -*-

__all__ = ['Response']


class Response(object):

    status = "200 OK"

    def __init__(self, output="", request=None):
        self.output = output
        self.request = request
        self.response_headers = [('Content-Type', 'text/html')]

    def __call__(self, environ, start_response):
        output = self.output if self.status.split(' ', 1)[0] == '200' else self.html
        response_headers = self.response_headers
        response_headers.append(('Content-Length', str(len(output))))
        start_response(self.status, response_headers)
        return [output]
