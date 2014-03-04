# -*- coding:utf-8 -*-

import Cookie
import datetime

__all__ = ['Response']


class Response(object):

    status = "200 OK"

    def __init__(self, output="", request=None):
        self.output = output
        self.request = request
        self.cookies = Cookie.SimpleCookie()
        self.response_headers = [('Content-Type', 'text/html')]

    def __call__(self, environ, start_response):
        output = self.output if self.status.split(' ', 1)[0] == '200' else self.html
        response_headers = self.response_headers
        response_headers.extend(tuple(cookie.split(':', 1)) for cookie in self.cookies.output().split('\r\n') if cookie)
        response_headers.append(('Content-Length', str(len(output))))
        start_response(self.status, response_headers)
        return [output]

    def set_cookie(self, name, value, domain=None, path='/', expires=None,
                   max_age=None, secure=None, httponly=None, version=None):
        self.cookies[name] = value
        self.cookies[name]["path"] = path
        if domain:
            self.cookies[name]["domain"] = domain
        if expires:
            expiration = datetime.datetime.now() + datetime.timedelta(days=expires)
            self.cookies[name]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        if max_age:
            self.cookies[name]["max-age"] = max_age
        if secure:
            self.cookies[name]["secure"] = secure
        if httponly:
            self.cookies[name]["httponly"] = httponly
