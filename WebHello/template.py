# -*- coding:utf-8 -*-

import re
from os.path import join

__all__ = ["Lookup", "Template"]
BLOCK_INVOKE_RE = re.compile("xxx")
EVA_CONTEXT_RE = re.compile(r'''
(
  {(?P<mark>[\^\$@=#])
    \s*(?P<statement>.*?)
  (?P=mark)}
|
  {%
    \s*(?P<director>(for|if))\s+(?P<director_info>.*?)\s*
  %}
  (?P<director_body>.*?)
  {%
    \s*end(?P=director)\s*
  %}
)
''', re.VERBOSE | re.DOTALL)
FOR_STATEMENT_RE = re.compile(r'''
^
  (?P<item>(?:\w+)(?:\s*,\s*\w+)?)\s*in\s*(?P<items>.*?)
$
''', re.VERBOSE | re.DOTALL)
IF_STATEMENT_RE = re.compile(r'''
^
(?P<if_statement>.*?)
(?P<elif_directors>
  (?:{%\s*elif\s+(?:.*?)%}
     (?:.*?)
  )*
)
({%\s*(?P<else_director>else)\s*%}
  (?P<else_statement>.*?)
)?
$
''', re.VERBOSE | re.DOTALL)
ELIF_STATEMENT_RE = re.compile(r'''
{%\s*elif\s+(?P<elif_director>.*?)%}(?P<elif_statement>.*?)(?=(?:$|{%\s*elif))
''', re.VERBOSE | re.DOTALL)


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
                output += str(eval(statement, self.namespace))
            elif mark == "$":
                statement = match.group('statement').strip()
                _match = BLOCK_INVOKE_RE.match(statement)
                block = self.template.blocks[_match.group('block')]
                _namespace = eval(statement, {k: v for k, v in block.signature.items()})
                block.render(_namespace)
            elif not mark:
                director = match.group('director').strip()
                director_info = match.group('director_info')
                director_body = match.group('director_body')
                if director == "for":
                    output += self.statement_for(director_info, director_body)
                elif director == "if":
                    output += self.statement_if(director_info, director_body)
            last_pos = match.end()
        return output + self.source[last_pos:]

    def statement_for(self, director_info, director_body):
        output = ""
        _match = FOR_STATEMENT_RE.match(director_info)
        _item = _match.group('item')
        items = eval(_match.group('items'), self.namespace)
        for item in items:
            self.namespace['__WEB_HELLO_FOR_EVA__'] = item
            exec "%s = __WEB_HELLO_FOR_EVA__" % _item in self.namespace
            del self.namespace['__WEB_HELLO_FOR_EVA__']
            output += EvaluationContext(self.template, director_body, self.namespace).render()
        return output

    def statement_if(self, director_info, director_body):
        output, solved = "", False
        match = IF_STATEMENT_RE.match(director_body)
        if_statement = match.group('if_statement')
        else_director = match.group('else_director')
        else_statement = match.group('else_statement')
        elifs = ELIF_STATEMENT_RE.findall(match.group('elif_directors'))
        if eval(director_info, self.namespace):
            solved = True
            output = EvaluationContext(self.template, if_statement, self.namespace).render()
        else:
            for director, statement in elifs:
                if eval(director, self.namespace):
                    solved = True
                    output = EvaluationContext(self.template, statement, self.namespace).render()
                    break
        if not solved and else_director:
            output = EvaluationContext(self.template, else_statement, self.namespace).render()
        return output


class RenderBlock(object):

    def __init__(self, template, raw_source):
        self.template = template
        self.raw_source = raw_source
        self.parse_raw_source()

    def parse_raw_source(self):
        self.name = ""
        self.signature = {}
        exec "def %s:return locals()" % self.raw_signature in self.signature

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
