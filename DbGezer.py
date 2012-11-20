#!/usr/bin/env python

from SharedPage import SharedPage

loginStoredPage = SharedPage.get_or_insert(LOGIN_PAGE_HTML_PATH)
iAgreeStoredPage = SharedPage.get_or_insert(I_AGREE_PAGE_HTML_PATH)

def checkPagesHash(name, value, exceptToRaise):
    page = SharedPage.get_or_insert(name)
    if not page.hashVal:
        page.hashVal = hash(value)
        page.put()
    elif page.hashVal != hash(value):
        raise exceptToRaise
