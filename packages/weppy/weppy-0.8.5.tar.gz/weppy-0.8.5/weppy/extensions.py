# -*- coding: utf-8 -*-
"""
    weppy.extensions
    ----------------

    Provides base classes to create extensions.

    :copyright: (c) 2014-2016 by Giovanni Barillari
    :license: BSD, see LICENSE for more details.
"""

from ._compat import iteritems


class Extension(object):
    namespace = None
    default_config = {}

    def __init__(self, app, env, config):
        self.app = app
        self.env = env
        self.config = config
        self.__init_config()

    def __init_config(self):
        for key, dval in iteritems(self.default_config):
            self.config[key] = self.config.get(key, dval)

    def on_load(self):
        pass


class TemplateExtension(object):
    namespace = None
    file_extension = None
    lexers = {}

    def __init__(self, env, config):
        self.env = env
        self.config = config

    def preload(self, path, name):
        return path, name

    def preprocess(self, source, name):
        return source

    def inject(self, context):
        pass


class TemplateLexer(object):
    evaluate_value = True

    def __init__(self, extension):
        self.ext = extension

    def __call__(self, parser, value=None):
        self.parser = parser
        if self.evaluate_value and value is not None:
            value = eval(value, self.parser.context)
        self.process(value)

    @property
    def stack(self):
        return self.parser.stack

    @property
    def top(self):
        return self.parser.stack[-1]

    def process(self, value):
        return value
