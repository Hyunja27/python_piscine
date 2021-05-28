#!/usr/bin/python3

from elements import Elem, Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br
from elem import Text


class Page:
    def __init__(self, elem) -> None:
        if not isinstance(elem, Elem) or type(elem) == Elem:
            raise Elem.ValidationError()
        self.elem = elem

    def is_valid(self):
        if self.check_all(self.elem) == True:
            return False
        return True

    def __str__(self):
        rt = str(self.elem)
        if not isinstance(self.elem, Html):
            return rt
        return "<!DOCTYPE html>\n" + rt

    def write_to_file(self, name: str):
        rt = str(self.elem)
        fd = open(name, 'w')
        if not isinstance(self.elem, Html):
            fd.write("<!DOCTYPE html>\n" + rt)
        else:
            fd.write(rt)
        fd.close()

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

        if isinstance(elem, (Body, Div)) == True:
            for i in elem.content:
                if isinstance(i, (H1, H2, Div, Table, Ul, Ol, Span, Text)) == False:
                    return True
                if all([self.check_all(k) for k in elem.content]):
                    return True

        if isinstance(elem, (Title, H1, H2, Li, Th, Td)) == True:
            ok = -1
            for i in elem.content:
                if isinstance(i, Text) == True:
                    ok += 1
                else:
                    return True
                if ok > 0:
                    return True
            # for k in elem.content:
            #         if self.check_all(k) == True:
            #             return True

        if isinstance(elem, P) == True:
            for i in elem.content:
                if isinstance(i, Text) == False:
                    return True

        if isinstance(elem, Span) == True:
            ok = -1
            for i in elem.content:
                if isinstance(i, (Text, P)) == False:
                    return True

        if isinstance(elem, (Ul, Ol)) == True:
            if len(elem.content) == 0:
                return True
            for i in elem.content:
                if isinstance(i, Li) == False:
                    return True

        if isinstance(elem, Tr) == True:
            th = 0
            td = 0
            for i in elem.content:
                if isinstance(i, Th) == True:
                    if td == 1:
                        return True
                    th = 1
                if isinstance(i, Td) == True:
                    if th == 1:
                        return True
                    td = 1

        if isinstance(elem, Table) == True:
            for i in elem.content:
                if isinstance(i, Tr) == False:
                    return True


def tester():
    print("\n====================================\n")
    print("\n=                                  =\n")
    print("\n=   Wellcome To Spark's Tester!    =\n")
    print("\n=                                  =\n")
    print("\n====================================\n")
    print("\n   It's For ctl + C / ctl + v     ..\n")
    print("\n   So, please enter Proper input!   \n")
    print("\n   (It's Not a minishell..zz)   \n")
    print("\n====> Enter your Test line!  :)\n")
    t = ""
    while t != "exit":
        t = input()
        if len(t) < 2:
            print("Bye!")
            return
        p = Page(eval(t))
        print(p.is_valid())
        print("\n\n------------------------------------\n")
        print("\n\n------------------------------------\n")
        print("\n====> Enter your Test line!  :)\n")


def main():
    tester()
    # p = Page(H1(Text("HEllo")))
    # print(p)
    # print(p.is_valid())


if __name__ == '__main__':
    main()
