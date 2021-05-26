#!/bin/python3

class Text(str):
    def __str__(self):
        return super().__str__().replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('\n', '\n<br />\n')


class Elem:
    class ValidationError(Exception):
        def __init__(self):
            super().__init__("Elem has Exception!")

    def __init__(self, tag='div', attr={}, content=None, tag_type='double'):
        self.tag = tag
        self.attr = attr
        if not (Elem.check_type(content) or content is None):
            raise Elem.ValidationError
        self.content = []
        if type(content) == list:
            self.content = content
        elif content is not None:
            self.content.append(content)
        self.tag_type = tag_type

    def __str__(self):
        temp1 = ("<{tag}{attr}>{content}</{tag}>")
        temp2 = ("<{tag}{attr}/>")
        rt = ""
        if self.tag_type == 'double':
            rt = self.__make_content()
            return temp1.format(tag=self.tag, attr=self.__make_attr(), content=rt)
        elif self.tag_type == 'simple':
            return temp2.format(tag=self.tag, attr=self.__make_attr())

    def __make_attr(self):
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        if len(self.content) == 0:
            return ''
        result = "\n"
        for elem in self.content:
            if (len(str(elem)) != 0):
                result += "{elem}\n".format(elem=elem)
        result = "  ".join(result.splitlines(True))
        if len(result.strip()) == 0:
            return ''
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))

if __name__ == '__main__':
    target = Elem('html', content=[
            Elem('head', content=
            Elem('title', content=
            Text('"Hello ground!"'))), 
            Elem('body', content=[Elem('h1', content=Text('"Oh no, not again!"')), Elem('img', {'src':'http://i.imgur.com/pfp3T.jpg'}, tag_type='simple')])])
    print(target)
