# -*- coding:utf-8 -*-

from WebHello.template import Lookup

from config import TEMPLATE_BASE


lookup = Lookup(TEMPLATE_BASE)
serve_template = lookup.serve_template
