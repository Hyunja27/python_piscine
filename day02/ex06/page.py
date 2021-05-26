#!/usr/bin/python3

from elements import Elem, Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br


class Page:
    def __init__(self, elem) -> None:
        if not isinstance(elem, Elem) or type(elem) == Elem:
            raise Elem.ValidationError()
        self.elem = elem

    def is_valid(self):
        if self.check_all(self.elem) == True:
            return False
        return True

    def check_all(self, elem):
        if not isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th,
                     Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)):
            return True

        if isinstance(elem, Html) == True:
            if not (len(elem.content) == 2 and isinstance(elem.content[0], Head) and
                                         isinstance(elem.content[1], Body)):
                return True
            else:
                for i in elem.content:
                    if self.check_all(i) == True:
                        return True
        
        if isinstance(elem, Head) == True:
            ok = -1
            for i in elem.content:
                if isinstance(i, Title) == True:
                    ok += 1
                if ok > 0:
                    return True
            for k in elem.content:
                    if self.check_all(k) == True:
                        return True
        
        # if isinstance(elem, Head) == True:
        

    def write_to_file(self, name: str):
        fd = open(str, 'r')


def main():
    p = Page(Html([Head(Title(), Title()), Body()]))

    print(p.is_valid())

if __name__ == '__main__':
    main()
