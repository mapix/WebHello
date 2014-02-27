# -*- coding:utf-8 -*-

urls = [
    ("/", "views.hello:say_hello"),
    ("/hello/{name:\w+}/", "views.hello:say_hello"),
]
