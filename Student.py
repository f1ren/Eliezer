#!/usr/bin/env python

class Student(db.Model):
    username = db.StringProperty()
    loginReq = db.StringProperty()
    lastHash = db.IntegerProperty()
    email = db.StringProperty()
    email_approved = db.BooleanProperty()
    email_approval_code = db.StringProperty()
