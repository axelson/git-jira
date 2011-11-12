#!/usr/bin/env python
from subprocess import Popen
from subprocess import PIPE

def run(command):
    #TODO: Detect if this command puts anything to stderr
    #print "running %s " % command
    commandUni = to_unicode_or_bust(command)
    pipe = Popen(unicode.split(commandUni), stdout=PIPE, stderr=PIPE)
    output = pipe.stdout.read()
    return output

def to_unicode_or_bust(
        obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
