#!/usr/bin/env python

from google.appengine.ext import db

class Student(db.Model):
    """Models a student with user name, ID and a password"""
    username = db.StringProperty()
    id_num = db.StringProperty()
    password = db.StringProperty()
    lastHTMLHash = db.IntegerProperty()
    email = db.StringProperty()
    email_approved = db.BooleanProperty()
    email_approval_code = db.StringProperty()

class HTML(db.Model):
    """Models a student with user name, ID and a password"""
    filename = db.StringProperty()
    hashVal = db.IntegerProperty()
