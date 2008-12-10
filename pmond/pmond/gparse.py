
"""
Parses gmond-style xml
"""

from lxml import etree

class gparse:
    def __init__():
        self.hosts = []

    def parse_string(s):
        root = etree.XML(s)
        print etree.tostring(root)


if __name__ == '__main__':
    f = open('test.xml')
    data = f.read()
    f.close()

    g = gparse()
    g.parse_string(data)
