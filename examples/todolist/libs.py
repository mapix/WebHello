# -*- coding:utf-8 -*-

from WebHello.template import Template

from config import TEMPLATE_BASE


template = Template(TEMPLATE_BASE)
st = serve_template = template.serve_template
