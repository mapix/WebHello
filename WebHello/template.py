# -*- coding:utf-8 -*-

import re
from os.path import join

__all__ = ["Lookup", "Template"]

RENDER_BLOCK_RE = re.compile("")
EVA_CONTEXT_RE = re.compile(r'''
    {
     (?P<mark>[%#=])
      (?P<statement>.*)
     (?P=mark)
    }''', re.VERBOSE)
SIGNATURE_RE = re.compile("")


class EvaluationContext(object):

    def __init__(self, template, source, namespace):
        self.template = template
        self.source = source
        self.namespace = namespace

    def render(self):
        output, last_pos = "", 0
        for match in EVA_CONTEXT_RE.finditer(self.source):
            output += self.source[last_pos:match.start()]
            mark = match.group('mark')
            if mark == "=":
                statement = match.group('statement').strip()
                output += eval(statement, self.namespace)
            last_pos = match.end()
        return output + self.source[last_pos:]


class RenderBlock(object):

    def __init__(self, template, raw_source):
        self.template = template
        self.raw_source = raw_source
        self.parse_raw_source()

    def parse_raw_source(self):
        name, signature = "", "" #TODO
        self.name = name
        self.signature = signature

    def make_context(self, namespace):
        #TODO filter with signature
        return EvaluationContext(self.template, self.source, namespace)

    def render(self, namespace):
        context = self.make_context(self, namespace)
        return context.render()


class Template(object):

    def __init__(self, filename, raw_source):
        self.filename = filename
        self.raw_source = raw_source
        self.parse_raw_source()

    def parse_raw_source(self):
        #raw_source, raw_blocks, last_pos = self.raw_source, [], 0
        #for match in RENDER_BLOCK_RE.finditer(content):
        #    raw_source += content[last_pos:match.start()])
        #    raw_blocks.append(RenderBlock(self, match.group(0)))
        #    last_pos = match.end()
        #source += content[last_pos:]
        #SIGNATURE_RE.sub(source, '')
        # self.signature = signature
        #self.source = source
        #self.blocks = {block.name: block for block in blocks}
        self.source = self.raw_source

    def make_context(self, namespace):
        #TODO filter with signature
        return EvaluationContext(self, self.source, namespace)

    def render(self, namespace):
        context = self.make_context(namespace)
        return context.render()


class Lookup(object):

    def __init__(self, template_base, **config):
        self.template_base = template_base
        self.config = config

    def serve_template(self, template_file, **kwargs):
        filename = join(self.template_base, template_file)
        with open(filename) as f:
            raw_source = f.read()
        template = Template(filename, raw_source)
        return template.render(kwargs)

    def serve_template_func(self, template_file, block, **kwargs):
        filename = join(self.template_base, template_file)
        with open(filename) as f:
            raw_source = f.read()
        template = Template(filename, raw_source)
        block = template.blocks[block]
        return block.render(kwargs)
