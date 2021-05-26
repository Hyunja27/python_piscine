#!/usr/bin/python3

from elem import Elem


class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(self, tag='html', attr=attr, content=content, tag_type='double')


print(Html(Elem()))
