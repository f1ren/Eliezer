#!/usr/bin/env python

import string
import random
import logging
from datetime import datetime

from google.appengine.ext import db
from google.appengine.api import mail

from Gezer import Gezer
from Student import Student

from Exceptions import *

#TODO load CHANGE_NOTIFICATION from file (template?)
CHANGE_NOTIFICATION = ["""There is some change in your exams on gezer.<br><br><br>
<font size=1><a href=%s/pages/unregistration.htm>unregister from Eliezer</a></font>""",
"""There is some change in your exams on gezer.
https://gezer1.bgu.ac.il/meser/entrance.php?uname=%s&passwd=%s&id=%s


To unregister from eliezer:
%s/pages/unregistration.htm"""]

class StudentsAdmin(object):
    def __init__(self, url):
        self.url = url
        self.gezer = Gezer()

    def sendHTMLEmail(self, to, subject, plaintext, html):
        message = mail.EmailMessage(
                sender="Eliezer BGU <navatm@gmail.com>",
                subject=subject)    
        message.to = to
        message.body = plaintext
        message.html = html
        message.send()
        logging.debug("Email was sent to %s" % to)

    def askStudentEmailApproval(self, student):
        email_approval_code = ''.join(random.choice(
            string.ascii_lowercase + string.digits)
            for x in range(10))

        approvalAddress = "%s/approve?email=%s&code=%s" % \
            (self.url,
             student.email,
             email_approval_code)

        mail.send_mail(sender="Eliezer BGU <navatm@gmail.com>",
                to=student.email,
                subject="Eliezer email confirmation",
                body="To complete the registration for user %s, "
                "please click the following link: %s"
                % (student.username, approvalAddress))

        # Wait for approval
        student.email_approved = False
        student.email_approval_code = email_approval_code

    def register(self, uname, password, id_num, email):
        # Attempt login
        self.gezer.login(uname, password, id_num)

        logging.debug("Successfully logged in as %s" % uname)

        # Save all info in a Student
        newStudent = Student()
        newStudent.username = uname
        newStudent.loginRequest = self.gezer.getLastLoginRequest()
        newStudent.lastHash = self.gezer.getLastExams().getHash()
        newStudent.email = email

        self.askStudentEmailApproval(newStudent)

        newStudent.put()

    def examsHashHasChanged(self, student, newHash):
        logging.info("change in exams of %s" % student.username)
        student.lastHash = newHash
        student.put()
        logging.debug("datetime.now().hour = %d" % datetime.now().hour)
        if datetime.now().hour in [4,5]:
            logging.debug("Too early")
        else:
            self.sendHTMLEmail(
                student.email,
                "Exams change on Gezer!",
                CHANGE_NOTIFICATION[1],
                CHANGE_NOTIFICATION[0],
                )

    def checkExams(self):
        students =  db.GqlQuery("SELECT * "
                                "FROM Student "
                                "WHERE email_approved = True")
        for student in students:
            logging.debug(student.username)
            try:
                self.gezer.updateExams(student.loginRequest)
                newHash = self.gezer.getLastExams().getHash()
                if newHash != student.lastHash:
                    self.examsHashHasChanged(student, newHash)
                else:
                    logging.debug("No change for %s" % student.username)
            except LoginExpiredException as e:
                student.delete()
                regAddress = "%s/pages/registration.htm" % self.url
                self.sendHTMLEmail(student.email,
                        "You were dropped of Eliezer!",
                        "Please <a href=%s>register again</a>." % regAddress,
                        "You can register again at %s" % regAddress)
            except Exception as e:
                logging.warn("User %s raised: %s" % (student.username, e.message))
