""":mod:`linky.sub` --- Substitude URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import functools
import re

from markupsafe import escape as html_escape

__all__ = 'Element', 'HTMLBuilder', 'linkfy', 'url_schema'
URL_REGEXP = r'(?P<url>' \
    r'(https?\:\/\/)?' \
    r'(www\.)?' \
    r'([^\s\.][^\s:]*\.[^\s/][^\s/]*(:[\d]+)?)' \
    r'(\/\S*)?' \
    r'(\?[\w\d=&]+)?(#[\w\-]*)?)'
url_schema = re.compile(URL_REGEXP)


class Element(object):

    def __init__(self, name, body=None, attributes={}, **kwargs):
        self.name = name
        self.body = body
        self.attributes = attributes
        self.attributes.update(kwargs)

    def __str__(self):
        attrs = ' '.join(
            '{}="{}"'.format(n, v)
            for n, v in self.attributes.items()
        )
        if self.body:
            html = '<{0} {2}>{1!s}</{0}>'.format(self.name, self.body, attrs)
        else:
            html = '<{0} {1}>'.format(self.name, attrs)
        return html


class HTMLBuilder(object):

    def __getattr__(self, name):
        return functools.partial(Element, name=name)


def linkfy(text, escape=True, **attributes):
    html = HTMLBuilder()
    words = []
    skip_parts = 0
    for w in url_schema.split(text):
        if skip_parts:
            skip_parts -= 1
            continue
        search = url_schema.search(w)
        if search and search.group('url') == w:
            t = str(html.a(href=w, body=w, **attributes))
            skip_parts = 7
        elif escape:
            t = html_escape(w)
        else:
            t = w
        words.append(t)
    return ''.join(words)
