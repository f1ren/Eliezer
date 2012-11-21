#!/usr/bin/env python

from google.appengine.ext import db

class Student(db.Model):
    username = db.StringProperty()
    loginRequest = db.BlobProperty()
    lastHash = db.IntegerProperty()
    email = db.StringProperty()
    email_approved = db.BooleanProperty()
    email_approval_code = db.StringProperty()
