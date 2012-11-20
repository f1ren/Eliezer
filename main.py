#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import db
from data import Student
from Exams import Exams
from Exams import *
import logging
import random
import string
from google.appengine.api import mail
from datetime import datetime

#TODO load CHANGE_NOTIFICATION from file (template?)
CHANGE_NOTIFICATION = ["""There is some change in your exams on gezer.<br>
<a href=https://gezer1.bgu.ac.il/meser/entrance.php?uname=%s&passwd=%s&id=%s>Open my gezer</a><br><br><br><br><br>
<font size=1><a href=%s/pages/unregistration.htm>unregister from Eliezer</a></font>""", """There is some change in your exams on gezer.
https://gezer1.bgu.ac.il/meser/entrance.php?uname=%s&passwd=%s&id=%s


To unregister from eliezer:
%s/pages/unregistration.htm"""]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        """
        navatm = Student()
        navatm.username = "navatm"
        navatm.id_num = "301227146"
        navatm.lastHTMLHash = 0
        navatm.put()
        """
        pass
def sendHTMLEmail(to, subject, plaintext, html):
    message = mail.EmailMessage(sender="Eliezer BGU <navatm@gmail.com>",
                                subject=subject)    
    message.to = to
    message.body = plaintext
    message.html = html
    message.send()
    logging.debug("Email was sent to %s" % to)

class CheckExamsHandler(webapp2.RequestHandler):
    def get(self):
        students =  db.GqlQuery("SELECT * "
                                "FROM Student "
                                "WHERE email_approved = True")
        for student in students:
            logging.debug(student.username)
            #self.response.out.write("<tr><td>%s</td><td>%s</td>" %
            #        (student.username, student.id_num))
            try:
                exams = Exams(student.username, student.id_num,
                            student.password)
                if not student.lastHTMLHash:
                    logging.debug("Setting hash")
                    student.lastHTMLHash = exams.getHash()
                    student.put()
                elif exams.getHash() != student.lastHTMLHash:
                    logging.info("change in exams of %s" % student.username)
                    student.lastHTMLHash = exams.getHash()
                    student.put()
                    #mail.send_mail(sender="Eliezer BGU <navatm@gmail.com>",
                    #        to=student.email,
                    #        subject="Gezer exams notification!",
                    #        body="""There is some change in your exams on gezer.
    #https://gezer1.bgu.ac.il/meser/entrance.php?uname=%s&passwd=%s&id=%s""" % (student.username, student.password, student.id_num))
                    logging.debug("datetime.now().hour = %d" % datetime.now().hour)
                    if datetime.now().hour in [4,5]:
                        logging.debug("Too early")
                    else:
                        sendHTMLEmail(
                            student.email,
                            "Exams change on Gezer!",
                            CHANGE_NOTIFICATION[1] % (student.username, student.password, student.id_num, self.request.application_url),
                            CHANGE_NOTIFICATION[0] % (student.username, student.password, student.id_num, self.request.application_url))
            except Exception as e:
                logging.warn("User %s raised: %s" % (student.username, e.message))

class UnregisterHandler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        id_num = self.request.get('id_num')
        email = self.request.get('email')
        gql =   "SELECT * " \
                "FROM Student " \
                "WHERE username = '%s' " \
                "AND id_num = '%s' " \
                "AND email = '%s'" % (username, id_num, email)
        students =  db.GqlQuery(gql)
        user_removed = False
        for student in students:
            student.delete()
            self.response.out.write("User unregistered<br>")
            user_removed = True
            logging.info("user %s unregistered" % username)
        if not user_removed:
            self.response.out.write("Could not find user")
            logging.info("Could not find user %s" % username)

class RegisterHandler(webapp2.RequestHandler):
    def post(self):
        email_approval_code = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))
        newStudent = Student()
        newStudent.username = self.request.get('username')
        newStudent.email = self.request.get('email')
        newStudent.email_approved = False
        newStudent.email_approval_code = email_approval_code
        newStudent.put()

        logging.info("user %s registered" % newStudent.username)

        approvalAddress = "%s/approve?email=%s&code=%s" % \
            (self.request.application_url,
             newStudent.email,
             email_approval_code)

        mail.send_mail(sender="Eliezer BGU <navatm@gmail.com>",
                to=newStudent.email,
                subject="Eliezer email confirmation",
                body="""To complete the registration for user %s, please click the following link:
%s""" % (newStudent.username, approvalAddress))

        self.response.out.write("A confirmation mail will be sent to you shortly.<br>")
        self.response.out.write("Please confirm your email address.<br>")

class ApprovalHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")
        approval_code = self.request.get("code")
        students =  db.GqlQuery("SELECT * "
                                "FROM Student "
                                "WHERE email = '%s'" % email)
        for student in students:
            if student.email_approval_code == approval_code:
                student.email_approved = True
                student.put()
                self.response.out.write("Ok, all done. You will receieve notifications about future changes in your exams.")
                logging.info("address %s confirmed" % email)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/checkExams', CheckExamsHandler),
                               ('/unregister', UnregisterHandler),
                               ('/register', RegisterHandler),
                               ('/approve', ApprovalHandler)],
                              debug=True)
