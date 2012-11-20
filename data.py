#!/usr/bin/env python

from google.appengine.ext import db

class SharedPage(db.Model):
    """
    Login pages that are shared to all students
    Practically it's:
        1. The form of user, password and id
        2. The I agree screen
    """
    pageName = db.StringProperty()
    hashVal = db.IntegerProperty()
