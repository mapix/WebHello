# -*- coding:utf-8 -*-


import cgi
import cgitb
import Cookie
from collections import defaultdict
from tempfile import TemporaryFile
cgitb.enable()

__all__ = ['Request']


class Request(object):

    def __init__(self, environ, **config):
        self.environ = environ
        self.config = config
        self.files = {}
        self.params = defaultdict(list)
        self._prepare_request()

    def _prepare_request(self):
        fields = cgi.FieldStorage(fp=self.environ['wsgi.input'], environ=self.environ, keep_blank_values=1)
        for field in fields.list:
            if isinstance(field.file, file):
                self.files[field.name] = (field.type, self._save_upload(field.file))
            else:
                self.params[field.name].append(field.value)
        self.cookies = Cookie.SimpleCookie(self.environ["HTTP_COOKIE"])

    def get_cookie(self, name):
        return self.cookies["session"].value

    def get_var(self, name, default=None):
        values = self.params.get(name)
        return values[-1] if values else default

    def get_list_var(self, name):
        return self.params.get(name) or []

    def get_method(self):
        return self.environ['REQUEST_METHOD']

    def get_path_info(self):
        return self.environ['PATH_INFO']

    def get_scheme(self):
        return self.environ.get('HTTP_X_FORWARDED_SCHEME', self.environ['wsgi.url_scheme'])


    def get_url(self):
        port = self.environ['SERVER_PORT']
        scheme = self.get_scheme()
        return "%s://%s%s%s%s%s" % (scheme, self.environ['SERVER_NAME'],
                              '' if (port == "80" and scheme == "http" or
                                     port == "443" and scheme == "https") else ":%s" % port,
                              self.environ['SCRIPT_NAME'],
                              self.environ['PATH_INFO'],
                              self.environ['QUERY_STRING'])

    def _save_upload(self, upload_file):
        fp = TemporaryFile()
        fp.write(upload_file.read())
        return fp

    def get_upload_type(self, name):
        if name not in self.files:
            raise Exception("")
        return self.files[name][0]

    def get_upload_content(self, name):
        if name not in self.files:
            raise Exception("")
        fp = self.files[name][1]
        fp.seek(0)
        return fp.read()
