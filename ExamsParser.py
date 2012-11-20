#!/usr/bin/env python

from bs4 import BeautifulSoup

CELLS_IN_ROW = 9

class ExamsParser(object):
    def __init__(self):
        self.fieldCounter = 0
    def feed(self, html):
        self.soup = BeautifulSoup(html)
    def _iterateTable(self, table):
        counter = 0
        nextExamFields = []
        for td in table.find_all('td'):
            counter += 1
            nextExamFields.append(td.string)
            if counter == 9:
                print nextExamFields
                counter = 0
                nextExamFields = []
    def getExams(self):
        for table in self.soup.find_all('table'):
            borderAtt = table.get("border")
            dirAtt = table.get("dir")
            if borderAtt == "1" and dirAtt == "rtl":
                self._iterateTable(table)

if __name__ == "__main__":
    ep = ExamsParser()
    ep.feed(open("lastExamsHtml.html", "rb").read())
    ep.getExams()
