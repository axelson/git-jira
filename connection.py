#!/usr/bin/python

import os.path
import sys
import getpass
from git_util import *
from cookies import *

'''This is a connection to jira'''
class connection:
    def __init__(self):
        #print "New connection"
        self.cookie = cookieHandler()
        #self.ensureLogin()

    def getPage(self, newurl):
        return self.cookie.getPage(newurl)

    def ensureLogin(self):
        #print "ensure login"
        if not(self.checkLogin()):
            self.doLogin()
            if not(self.checkLogin()):
                print "There was a stale cookie file, trying one more time after clearing session cookies"
                self.cookie.clearSessionCookies()
                self.cookie.saveCookies()
                self.doLogin()

    def getLoginUrl(self):
        #loginUrl = 'http://' + getGitValue('url') + '/rest/auth/latest/session'
        loginUrl = 'http://' + getGitValue('url') + '/rest/auth/1/session'
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
        loginUrl = self.getLoginUrl()
        #print "Logging in with %s and %s" % (username, password)
        print "Logging in to JIRA (%s) as %s" % (loginUrl, username)

        if (self.checkLogin()):
            # Already logged in
            # This method shouldn't be called if you are already logged in,
            # instead you should call ensureLogin if unsure
            print "ERROR: Already logged in, you should never see this in production!"
            return

        txdata = '{"username" : "' + username +'", "password" : "'+ password +'"}'
        txheaders =  {'Content-Type' : 'application/json'}
        req = self.cookie.Request(loginUrl, txdata, txheaders)
        try:
            handle = self.cookie.urlopen(req)
        except self.cookie.HTTPError as inst:
            #print "Unable to login due to < %s >" % inst
            if (inst.code == 401):
                #TODO: Check if this works when a cookie is expired
                print "Unable to login due to 401 error, possible stale cookie or shared cookie file"
                #print "Possible stale session (HTTP 401), attempting to login again"
                #print "New session disabled"
                return

        print handle.read()
        print
        self.cookie.saveCookies()
        if not(self.checkLogin()):
            print "ERROR, Unable to Login"

    def getCookie(self):
        '''Return a reference to the cookieHandler within'''
        return self.cookie
