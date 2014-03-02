# -*- coding:utf-8 -*-

import re
from os.path import join

__all__ = ["Template"]

RENDER_BLOCK_RE = re.compile()
EVA_BLOCK_RE = re.compile()


class RenderBlock(object):

    def __init__(self, name, signature, source, template):
        self.name = name
        self.signature = signature
        self.source = source
        self.template = template

    @classmethod
    def make_block(cls, name, raw_source, template):
        signature, source = cls.parse_raw_source(raw_source)
        return cls(name, signature, source, tempate)

    @classmethod
    def parse_raw_source(cls, raw_source):
        pass

    def make_context(self, **kwargs):
        return kwargs

    def render(self, **kwargs):
        container = self.make_context(**kwargs)
        output, last_pos = "", 0
        for match in EVA_BLOCK_RE.finditer(self.source):
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


class Template(RenderBlock):

    def __init__(self, name, signature, source):
        super(Template, self).__init__(name, signature, source, self)
        self.blocks = {}
        self.parse_sub_blocks()

    @classmethod
    def parse_template(cls, filename):
        with open(filename) as source_file:
            content = source_file.read()
        raw_source, raw_blocks, last_pos = "", [], 0
        for match in RENDER_BLOCK_RE.finditer(content):
            raw_source += content[last_pos:match.start()])
            raw_blocks.append(match.group(0))
            last_pos = match.end()
        source += content[last_pos:]
        signature, source = cls.parse_raw_source(raw_source)
        template = cls(filename, signature, source)
        template.blocks = {name: cls.make_block(name, raw_block, template)
                           for name, raw_block in raw_blocks}
        return template

    @classmethod
    def parse_raw_source(cls, raw_source):
        pass
