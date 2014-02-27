# -*- coding:utf-8 -*-

from libs.template import serve_template

def say_hello(request, name="mapix"):
    return serve_template('templates/hello.html', **locals())
