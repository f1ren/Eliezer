#!/usr/bin/env python

from SharedPage import SharedPage

def checkPagesHash(name, value, exceptToRaise):
    page = SharedPage.get_or_insert(name)
    if not page.hashVal:
        page.hashVal = hash(value)
        page.put()
    elif page.hashVal != hash(value):
        raise exceptToRaise
