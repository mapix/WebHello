# -*- coding:utf-8 -*-

def serve_template(filename, **kwargs):
    template = open(filename).read()
    return template.format(**kwargs)

