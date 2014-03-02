# -*- coding:utf-8 -*-

from os.path import join

__all__ = ["Template"]

class Template(object):

    def __init__(self, template_base, **config):
        self.template_base = template_base
        self.config = config

    def serve_template(self, filename, **kwargs):
        template = open(join(self.template_base, filename), 'r').read()
        return template.format(**kwargs)

