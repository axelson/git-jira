#!/usr/local/bin/python
# 2005/01/02
#v1.0.1 

# cookie_example.py
# An example showing the usage of cookielib (New to Python 2.4) and ClientCookie

# Copyright Michael Foord, 2004.
# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/documents/BSD-LICENSE.txt

# For information about bugfixes, updates and support, please join the Pythonutils mailing list.
# http://voidspace.org.uk/mailman/listinfo/pythonutils_voidspace.org.uk
# Comments, suggestions and bug reports welcome.
# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# E-mail fuzzyman@voidspace.org.uk

"""
cookielib is a library new to Python 2.4
Prior to Python 2.4 it existed as ClientCookie, but it's not a drop in replacement.
In Python 2.4 some of the function of ClientCookie has been made into modifications of urllib2

This example shows basic code for fetching URIs that will work unchanged on :
a machine with python 2.4 (and cookielib)
a machine with ClientCookie
a machine with neither
(Obviously on the machine with neither the cookies won't be handled or saved).

Where either cookielib or ClientCookie is available the cookies will be saved in a file.
If that file exists already the cookies will first be loaded from it.
The file format is a useful plain text format and the attributes of each cookie is accessible in the Cookiejar instance (once loaded).

This may be helpful to those just using ClientCookie as the ClientCookie documentation doesn't appear to document the LWPCookieJar class which is needed for saving and loading cookies.

*WHY*
I'm writing a cgi-proxy called approx.py (see www.voidspace.org.uk/atlantibots/pythonutils.html#cgiproxy ).
It remotely fetches webpages for those in a restricted internet environment.
If ClientCookie is available it will handle cookies (and works well) - including loading/saving a different set of cookies for each user.
My server has python 2.2 - but I'd like the script to function well on machines with Python 2.4 or without ClientCookie at all.
This code installs a Cookiejar and CookieProcessor as the default handler for urllib2.urlopen if these are available.
Otherwise calls to urlopen work as normal.

If the example works as it should then you'll see some page headers printed and then the cookie that the server sent you.
This should then be saved to a file 'cookies.lwp'
(of course you may need to install ClientCookie)

Of course this example also illustrates using Request objects and headers etc to fetch webpages....
"""

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

theurl = 'http://www.google.co.uk/search?hl=en&ie=UTF-8&q=voidspace&meta='         # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
txdata = None                                                                           # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}          # fake a user agent, some websites (like google) don't like automated exploration

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
    cj.save(COOKIEFILE)                     # save the cookies again

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
