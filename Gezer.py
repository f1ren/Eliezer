#!/usr/bin/env python

import mechanize
from utils import *
from Exceptions import *
from Exams import Exams
from DbGezer import *

LOGIN_URL = "https://gezer1.bgu.ac.il/teva/scomp.php"

LOGIN_PAGE_HTML_PATH = "loginPageHtml"
I_AGREE_PAGE_HTML_PATH = "iAgreePageHtml"

class Gezer(object):
    _exams = None
    _loginRequest = None

    def __init__(self, pageHashesCheckFunc = checkPagesHash):
        self.pageHashesCheckFunc = pageHashesCheckFunc

    def login(self, uname, passwd, id_num):
        br = mechanize.Browser()
        loginPage = br.open(LOGIN_URL)
        loginPageHtml = loginPage.read()

        # If it's first time to see a login page, save the hash
        self.pageHashesCheckFunc(LOGIN_PAGE_HTML_PATH, \
                loginPageHtml, LoginException("Login page has changed"))
                
        # Login
        br.select_form(nr=0)
        br["uname"] = uname
        br["passwd"] = passwd
        br["id"] = id_num
        iAgreePage = br.submit()
        iAgreeHtml = iAgreePage.read()

        # If it's first time to see the i agree page, save the hash
        self.pageHashesCheckFunc(I_AGREE_PAGE_HTML_PATH, \
                iAgreeHtml, LoginException("Login failed. Bad password?"))

        # Agree
        br.select_form(nr=0)
        examsTable = br.submit()

        # Store the login
        self._loginRequest = requestToStr(br.request)

        # Store the hash of the exams
        self._exams = Exams(examsTable.read())

    def updateExams(self, loginRequest):
        req = strToRequest(loginRequest)
        examsTable = mechanize.urlopen(req)

        examsHtml = examsTable.read()

        if len(examsHtml) <= 600:
            raise LoginExpiredException()

        self._exams = Exams(examsHtml)
        self._loginRequest = loginRequest

    def getLastExams(self):
        return self._exams

    def getLastLoginRequest(self):
        return self._loginRequest

# Unit test
stubHashTable = {}
def checkHashStub(name, value, exceptToRaise):
    if not stubHashTable.has_key(name):
        stubHashTable[name] = hash(value)
    elif stubHashTable[name] != hash(value):
        raise exceptToRaise

if __name__ == "__main__":
    g = Gezer(checkHashStub)
    password = raw_input("password")
    g.login("navatm", password, "301227146")
    h = g.getLastExams().getHash()
    g.updateExams(g.getLastLoginRequest())
    print g.getLastExams().html
    print h == g.getLastExams().getHash()
