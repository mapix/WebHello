# -*- coding:utf-8 -*-

import re
from os.path import join

__all__ = ["Template"]

RENDER_BLOCK_RE = re.compile()
EVA_CONTEXT_RE = re.compile()
SIGNATURE_RE = re.compile()

class EvaluationContext(object):

    def __init__(self, template, source, namespace):
        self.template = template
        self.source = source
        self.namespace = namespace

    def render(self):
        output, last_pos = "", 0
        for match in EVA_CONTEXT_RE.finditer(self.source):
            output += content[last_pos:match.start()])
            statement = match.group('statement').strip()
            if statement.beginswith('#'):
                block = self.blocks[statement[1:]]
                _kwargs = block.make_context(**kwargs)
                output += block.render(**_kwargs)
            else:
                output += eva(match.group('statement'), container)
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
        raw_source, raw_blocks, last_pos = self.raw_source, [], 0
        for match in RENDER_BLOCK_RE.finditer(content):
            raw_source += content[last_pos:match.start()])
            raw_blocks.append(RenderBlock(self, match.group(0)))
            last_pos = match.end()
        source += content[last_pos:]
        SIGNATURE_RE.sub(source, '')
        self.signature = signature
        self.source = source
        self.blocks = {block.name, block for block in blocks}

    def make_context(self, namespace):
        #TODO filter with signature
        context = EvaluationContext(self.template, self.source, namespace)
        return namespace

    def render(self, namespace):
        context = self.make_context(self, namespace)
        return context.render()
