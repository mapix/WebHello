# -*- coding:utf-8 -*-

from libs import serve_template

def say_hello(request, name="mapix"):
    action = request.get_var('action', 'eat')
    return serve_template('hello.html', **locals())

