#!/usr/bin/env python

class Elem():
    def __init__(self, name, atts=[]):
        self.nm = name
        self.atts = atts
        self.content = []

    def __str__(self):
        code = ("<{name}  {atts}>\n"
                "  {content}\n"
                "</{name}>")

        def list_to_content():
            return "  ".join("".join(str(val) for val in self.content).splitlines(True))

        return code.format(name=self.nm, atts=self.atts, content=list_to_content())

    def add_content(self, val):
        self.content.append(val)

    class Elem_Exception(Exception):
        def __init__(self):
            super().__init__("Elem_exception!")
#   <body  id=jaeskim>
#     hello!hello!
#   </body>

def main():
    a = Elem("html", "id='spark'")
    b = Elem("body", "id='jaeskim'")
    a.add_content(b)
    b.add_content("hello!")
    b.add_content("hello!")
    print(a)


if __name__ == '__main__':
    main()
