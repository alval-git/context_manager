class Tag:
    def __init__(self, tag, toplevel = False, is_single = False, **kwargs):
        self.tag = tag
        self.toplevel = toplevel
        self.is_single = is_single
        self.text = ""
        self.attributes = {}
        self.children = []
        for attr, value in kwargs.items():
            if attr == "klass":
                self.attributes[attr] = ' '.join(value)
            else:
                self.attributes[attr] = value
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __iadd__(self, other):
        self.children.append(other)
        return self
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append("{} = '{}'".format(attribute, value))
        attrs = " ".join(attrs)
        if len(self.attributes) != 0:
            line = "<{tag} {attrs}>".format(tag = self.tag, attrs = attrs)
        elif self.is_single and len(self.attributes) == 0:
            line = "<{tag}>".format(tag = self.tag)
        else:
            line = "<{tag}>".format(tag = self.tag)
        if self.children:
            for child in self.children:
                line += "\n"
                line += str(child)
        if not self.is_single:
            line += "\n"
            line += "{text}</{tag}>".format(tag = self.tag, text = self.text)

        else:
            line += ""
            line += "\n"
        return line
class HTML():
    def __init__(self, **kwargs):
        self.tag = "html"
        self.children = []
        for attr, value in kwargs.items():
            self.output = value
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        if self.output == None:
            print("<%s>" % self.tag)
            for child in self.children:
                print(str(child))
            print("</%s>" % self.tag)
        else:
            with open("my_html.html", "w") as f:
                f.write(str(self))
    def __iadd__(self, other):
        self.children.append(other)
        return self
    def __str__(self):
        line = "<html>"
        if self.children:
            for child in self.children:
                line += str(child)
        line += "</html>"
        return line
class TopLevelTag(Tag):
    pass
if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png") as img:
                    img.text = ""
                    div += img
                body += div
            doc += body






