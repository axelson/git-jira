#!/usr/bin/python

import os.path
import sys
import getpass
from git_util import *
from cookies import *

'''This is a connection to jira'''
class connection:
    def __init__(self):
        self.cookie = cookieHandler()
        #self.ensureLogin()

    def getPage(self, newurl):
        return self.cookie.getPage(newurl)

    def ensureLogin(self):
        #print "ensure login"
        if not(self.checkLogin()):
            self.doLogin()

    def getLoginUrl(self):
        loginUrl = 'http://' + getGitValue('url') + '/rest/auth/latest/session'
        return loginUrl

    def checkLogin(self):
        #TODO: This fails on an expired cookie
        #print "check login running"
        loginUrl = self.getLoginUrl()
        handle = None
        try:
            handle = self.cookie.getPage(loginUrl)
        except self.cookie.HTTPError, err:
            if(err.code == 401):
                #print "Check login return false"
                return False
            else:
                raise
        else:
            #print "Already logged in"
            return True

    def doLogin(self):
        username = getGitValue('username')
        password = getGitValue('password')
        #password = getpass.getpass()
        #password = 'hunter2'
        #TODO: Use correct url

        if (self.checkLogin()):
            # Already logged in
            print "Already logged in"
            return

        loginUrl = self.getLoginUrl()
        print "Logging in to JIRA (%s) as %s" % (loginUrl, username)
        txdata = '{"username" : "' + username +'", "password" : "'+ password +'"}'
        txheaders =  {'Content-Type' : 'application/json'}
        req = self.cookie.Request(loginUrl, txdata, txheaders)
        try:
            handle = self.cookie.urlopen(req)
        except self.cookie.HTTPError as inst:
            print "Unable to login due to < %s >" % inst
            self.cookie.clearSessionCookies()
            self.cookie.saveCookies()
            if (inst.code == 401):
                #TODO: Check if this works when a cookie is expired
                print "Possible stale session (HTTP 401), attempting to login again"
                print "New session disabled"
                self.doLogin()
                return

        print handle.read()
        print
        self.cookie.saveCookies()
        if not(self.checkLogin()):
            print "ERROR, Unable to Login"

    def getCookie(self):
        '''Return a reference to the cookieHandler within'''
        return self.cookie
