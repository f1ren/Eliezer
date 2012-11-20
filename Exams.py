#!/usr/bin/env python

import re

class Exams(object):
    def __init__(self, html):
        self.html = html
        for i in re.findall("token=.*?&", self.html):
            self.html = self.html.replace(i,"")
        for i in re.findall("timestamp=.*?\"", self.html):
            self.html = self.html.replace(i,"") 
        self.hashVal = hash(self.html)

    def getHash(self):
        return self.hashVal
