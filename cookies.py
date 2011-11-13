#!/usr/bin/python

COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
import os.path
import sys

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
            self.urlopen = urllib2.urlopen
            self.cj = cookielib.LWPCookieJar()
            self.Request = urllib2.Request

        if not cookielib:                   # If importing cookielib fails let's try ClientCookie
            try:
                import ClientCookie
            except ImportError:
                import urllib2
                urlopen = urllib2.urlopen
                Request = urllib2.Request
            else:
                urlopen = ClientCookie.urlopen
                self.cj = ClientCookie.LWPCookieJar()
                Request = ClientCookie.Request

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

    def getPage(self, newurl):
        req = self.Request(newurl)
        # create a request object
        handle = self.urlopen(req)
        print handle.info()


    def printCookies(self):
        print 'These are the cookies we have received so far :'
        for index, cookie in enumerate(cj):
            print index, '  :  ', cookie

    def saveCookies(self):
        cj.save(COOKIEFILE, ignore_discard=True)
