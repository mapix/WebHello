# -*- coding:utf-8 -*-

from os.path import curdir, abspath, dirname, join

APP_BASE = abspath(curdir)
WEB_HELLO_BASE = dirname(dirname(APP_BASE))
TEMPLATE_BASE = join(APP_BASE, "templates")

