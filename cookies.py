#!/usr/bin/python

COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
import os.path
import sys
from git_util import *

class cookieHandler:
    def __init__(self):
        self.cj = None
        self.ClientCookie = None
        cookielib = None

        try:                                    # Let's see if cookielib is available
            import cookielib
        except ImportError:
            pass
        else:
            import urllib2
            self.HTTPError = urllib2.HTTPError
            self.urlopen = urllib2.urlopen
            self.cj = cookielib.LWPCookieJar(COOKIEFILE)
            try:
                self.cj.load(ignore_discard=True)
            except IOError:
                pass
            self.Request = urllib2.Request

        if not cookielib:                   # If importing cookielib fails let's try ClientCookie
            try:
                import ClientCookie
            except ImportError:
                import urllib2
                self.HTTPError = urllib2.HTTPError
                self.urlopen = urllib2.urlopen
                self.Request = urllib2.Request
            else:
                # TODO This might not work, might need the import statement
                self.HTTPError = urllib2.HTTPError
                #import urllib2.HTTPError as self.HTTPError
                self.urlopen = ClientCookie.urlopen
                self.cj = ClientCookie.LWPCookieJar(COOKIEFILE)
                self.cj.load(ignore_discard=True)
                self.Request = ClientCookie.Request

        ####################################################
        # We've now imported the relevant library - whichever library is being used urlopen is bound to the right function for retrieving URLs
        # Request is bound to the right function for creating Request objects
        # Let's load the cookies, if they exist. 
        if self.cj == None:
            print "No cookie jar available! Unable to continue!"
            sys.exit(1)

        if self.cj != None:                                  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
            if os.path.isfile(COOKIEFILE):
                self.cj.load(COOKIEFILE)
            if cookielib:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
                urllib2.install_opener(opener)
            else:
                opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(self.cj))
                ClientCookie.install_opener(opener)

        print "going to ensure login"
        self.ensureLogin()

    def getPage(self, newurl):
        req = self.Request(newurl)
        # create a request object
        handle = self.urlopen(req)
        return handle

    def ensureLogin(self):
        print "ensure login"
        if not(self.checkLogin()):
            self.doLogin()

    def checkLogin(self):
        print "check login running"
        loginUrl = 'http://localhost:8080/rest/auth/latest/session'
        handle = None
        try:
            handle = self.getPage(loginUrl)
        except self.HTTPError, err:
            if(err.code == 401):
                return False
            else:
                raise
        else:
            print "logged in"
            #print handle.info()
            return True

    def doLogin(self):
        username = getGitValue('username')
        password = getGitValue('password')
        print "Logging in to JIRA as %s" % username
        loginUrl = 'http://localhost:8080/rest/auth/latest/session'
        txdata = '{"username" : "' + username +'", "password" : "'+ password +'"}'
        print txdata
        txheaders =  {'Content-Type' : 'application/json'}
        req = self.Request(loginUrl, txdata, txheaders)            # create a request object
        print "about to create handle"
        try:
            handle = self.urlopen(req)                               # and open it to return a handle on the url
        except:
            return
        print "created handle"
        print handle.read()
        self.saveCookies()
        print "login is now"
        print self.checkLogin()


    def printCookies(self):
        print 'These are the cookies we have received so far :'
        for index, cookie in enumerate(self.cj):
            print index, '  :  ', cookie

    def saveCookies(self):
        self.cj.save(COOKIEFILE, ignore_discard=True)
