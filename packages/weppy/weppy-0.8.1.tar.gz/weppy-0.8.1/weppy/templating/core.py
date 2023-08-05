# -*- coding: utf-8 -*-
"""
    weppy.templating.core
    ---------------------

    Provides the templating system for weppy.

    :copyright: (c) 2014-2016 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

import os
import cgi
import sys
from .._compat import StringIO, reduce, string_types, text_type, to_native, \
    to_unicode, to_bytes
from ..tags import asis
from ..helpers import load_component
from ..datastructures import sdict
from .parser import TemplateParser
from .cache import TemplaterCache
from .helpers import TemplateMissingError, TemplateReference


class DummyResponse():
    def __init__(self):
        self.body = StringIO()

    @staticmethod
    def _to_html(data):
        return to_bytes(data, 'ascii', 'xmlcharrefreplace')

    @staticmethod
    def _to_native(data):
        if not isinstance(data, text_type):
            data = to_unicode(data)
        return to_native(data)

    @staticmethod
    def _to_unicode(data):
        if not isinstance(data, string_types):
            return text_type(data)
        return to_unicode(data)

    def write(self, data, escape=True):
        body = None
        if escape:
            if hasattr(data, 'to_html'):
                try:
                    body = to_native(data.to_html())
                except:
                    pass
            if body is None:
                body = self._to_native(
                    self._to_html(
                        cgi.escape(
                            self._to_unicode(data), True
                        ).replace(u"'", u"&#x27;")))
        else:
            body = self._to_native(data)
        self.body.write(body)


class Templater(object):
    def __init__(self, application):
        self.loaders = application.template_preloaders
        self.renders = application.template_extensions
        self.lexers = application.template_lexers
        self.cache = TemplaterCache(application, self)

    def preload(self, path, name):
        fext = os.path.splitext(name)[1]
        return reduce(lambda s, e: e.preload(s[0], s[1]),
                      self.loaders.get(fext, []), (path, name))

    def load(self, path, filename):
        # return source as unicode str
        try:
            file_obj = open(os.path.join(path, filename), 'r')
            source = to_unicode(file_obj.read())
            file_obj.close()
        except IOError:
            raise TemplateMissingError(path, filename)
        return source

    def prerender(self, source, filename):
        return reduce(lambda s, e: e.preprocess(s, filename),
                      self.renders, source)

    def inject(self, context):
        for extension in self.renders:
            extension.inject(context)

    def parse(self, path, filename, source, context):
        code, parserdata = self.cache.get(filename, source)
        if not code:
            parser = TemplateParser(self, source, name=filename,
                                    context=context, path=path)
            code = compile(str(parser), filename, 'exec')
            parserdata = sdict(content=parser.content,
                               blocks=parser.content.blocks)
            self.cache.set(
                filename, source, code, parserdata, parser.included_templates)
        return code, parserdata

    def _render(self, source='', path=None, filename=None, context={}):
        if isinstance(context, sdict):
            context = dict(context)
        context['asis'] = context.get('asis', asis)
        context['load_component'] = context.get(
            'load_component', load_component)
        context['_DummyResponse_'] = DummyResponse()
        code, parserdata = self.parse(path, filename, source, context)
        self.inject(context)
        try:
            exec(code, context)
        except:
            from ..debug import make_traceback
            exc_info = sys.exc_info()
            try:
                parserdata.path = path
                parserdata.name = filename
                template_ref = TemplateReference(parserdata, code, exc_info[0],
                                                 exc_info[1], exc_info[2])
            except:
                template_ref = None
            context['__weppy_template__'] = template_ref
            make_traceback(exc_info, template_ref)
        return context['_DummyResponse_'].body.getvalue()

    def render(self, path, filename, context={}):
        tpath, tname = self.preload(path, filename)
        tsource = self.load(tpath, tname)
        tsource = self.prerender(tsource, tname)
        return self._render(tsource, tpath, tname, context)
