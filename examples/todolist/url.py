# -*- coding:utf-8 -*-

urls = [
    ("/", "views.hello:say_hello"),
    ("/hello/{name:\w+}/", "views.hello:say_hello"),
    ("/test_post", "views.test_post:test_post"),
]
