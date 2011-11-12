#!/usr/bin/python

COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
import os.path
import sys

cj = None
ClientCookie = None
cookielib = None

try:                                    # Let's see if cookielib is available
    import cookielib
except ImportError:
    pass
else:
    import urllib2
    urlopen = urllib2.urlopen
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    Request = urllib2.Request

if not cookielib:                   # If importing cookielib fails let's try ClientCookie
    try:
        import ClientCookie 
    except ImportError:
        import urllib2
        urlopen = urllib2.urlopen
        Request = urllib2.Request
    else:
        urlopen = ClientCookie.urlopen
        cj = ClientCookie.LWPCookieJar()
        Request = ClientCookie.Request

####################################################
# We've now imported the relevant library - whichever library is being used urlopen is bound to the right function for retrieving URLs
# Request is bound to the right function for creating Request objects
# Let's load the cookies, if they exist. 

if cj != None:                                  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    if cookielib:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

# If one of the cookie libraries is available, any call to urlopen will handle cookies using the CookieJar instance we've created
# (Note that if we are using ClientCookie we haven't explicitly imported urllib2)
# as an example :



theurl = 'http://localhost:8080/rest/auth/latest/session'
txdata = '{"username" : "jaxelson", "password" : "hunter2"}'
#txheaders =  {'Content-Type' : 'application/json', 'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
txheaders =  {'Content-Type' : 'application/json'}

try:
    req = Request(theurl, txdata, txheaders)            # create a request object
    handle = urlopen(req)                               # and open it to return a handle on the url
except IOError, e:
    print 'We failed to open "%s".' % theurl
    if hasattr(e, 'code'):
        print 'We failed with error code - %s.' % e.code
    elif hasattr(e, 'reason'):
        print "The error object has the following 'reason' attribute :", e.reason
        print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
        sys.exit()

else:
    print 'Here are the headers of the page :'
    print handle.info()                             # handle.read() returns the page, handle.geturl() returns the true url of the page fetched (in case urlopen has followed any redirects, which it sometimes does)

print
if cj == None:
    print "We don't have a cookie library available - sorry."
    print "I can't show you any cookies."
else:
    print 'These are the cookies we have received so far :'
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie        
    cj.save(COOKIEFILE, ignore_discard=True)                     # save the cookies again

# We can always tell which import was successful.
# If we are using cookielib then cookielib != None
# If we are using ClientCookie then ClientCookie != None
# If we are using neither then cj == None

# Request is the name bound to the appropriate function for creating Request objects
# urlopen is the name bound to the appropriate function for opening URLs
# *whichever* library we have used !!

"""

CHANGELOG
2005/02/14      Version 1.02
Corrected another typo and added import sys - blimey.

2005/01/02      Version 1.0.1
Corrected a couple of typos - 'urlib' to 'urllib2'.. oops.
Display the 'reason' attribute if fetching the page fails.

31-08-2004      Version 1.0.0
Released into the wild.
"""
