#!/usr/bin/env python

import mechanize
import time
import sys
import thread
import re
import md5
import logging
import webapp2
from data import *

# 10 minutes
SLEEP_TIME = 10*60 

GMAIL_USER = "notifyrobot1@gmail.com"
GMAIL_PASS = "notifyrobot"
TO = "navatm@gmail.com"

LAST_HTML_OUTPUT = "lastExamsHtml.html"

LOGIN_PAGE_HTML_PATH = "loginPageHtml.html"
I_AGREE_PAGE_HTML_PATH = "iAgreePageHtml.html"
I_AGREE_PAGE_HTML_PATH = "newiAgreePageHtml.html"

#LOGIN_PAGE_HTML = file(LOGIN_PAGE_HTML_PATH,'rb').read()
#I_AGREE_PAGE_HTML = file(I_AGREE_PAGE_HTML_PATH,'rb').read()

EXAMS_TABLE_MAGIC = "<input type=hidden name=moresemesters value=1>"

LOGIN_URL = "https://gezer1.bgu.ac.il/teva/scomp.php"

REWRITE_PAGES = False

class Exams(object):
    def __init__(self, username, id_num, password):
        self.loginPage = HTML.get_or_insert(LOGIN_PAGE_HTML_PATH)
        self.iAgreePage = HTML.get_or_insert(I_AGREE_PAGE_HTML_PATH)
        self.html = self.getExamsHTML(username, id_num, password)
        for i in re.findall("token=.*?&", self.html):
            self.html = self.html.replace(i,"")
        for i in re.findall("timestamp=.*?\"", self.html):
            self.html = self.html.replace(i,"") 
    def getHash(self):
        return hash(self.html)
    def getExamsHTML(self, username, id_num, password):
        br = mechanize.Browser()
        loginPage = br.open(LOGIN_URL)
        loginPageHtml = loginPage.read()
        if REWRITE_PAGES or not self.loginPage.hashVal:
            #file(LOGIN_PAGE_HTML_PATH,'wb').write(loginPageHtml)
            self.loginPage.hashVal = hash(loginPageHtml)
            self.loginPage.put()
        elif self.loginPage.hashVal != hash(loginPageHtml):
            raise Exception("Login page has changed")
                
        br.select_form(nr=0)
        br["uname"]= username
        br["passwd"]= password
        br["id"]= id_num
        iAgreePage = br.submit()
        iAgreeHtml = iAgreePage.read()
        if REWRITE_PAGES or not self.iAgreePage.hashVal:
            #file(I_AGREE_PAGE_HTML_PATH,'wb').write(iAgreeHtml)
            self.iAgreePage.hashVal = hash(iAgreeHtml)
            self.iAgreePage.put()
        elif self.iAgreePage.hashVal != hash(iAgreeHtml):
            raise Exception("Wrong I Agree page, probably bad password")

        br.select_form(nr=0)
        examsTable = br.submit()
        examsTableHtml = examsTable.read()
        #if examsTableHtml.find(EXAMS_TABLE_MAGIC)==-1:
        #    raise Exception("Failed finding magic in exams table")

        return examsTableHtml
