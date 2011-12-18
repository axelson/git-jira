#!/usr/bin/env python
import httplib
import urllib
import json
from util import *
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

# Targetting jira version Atlassian JIRA (v4.3.3#617-r149616)

# Settings
jira = 'localhost:8080'
jiraApi = '/rest/api/2.0.alpha1'
headers = {'Content-type': 'application/json','Accept': 'application/json'}

def setGitValue(name, value):
    run("git config %(prefix)s.%(name)s %(value)s" % {'prefix': 'jira', 'name': name, 'value': value})

def getGitValue(name):
    value = run("git config %(prefix)s.%(name)s" % {'prefix': 'jira', 'name': name})
    if(value == ''):
        #TODO throw some type of keyerror
        #print "ERROR: no value for %s" % name
        pass
    return value.strip()

def getBranchName():
    '''Return the name of the current branch'''
    # Expect output like 'refs/heads/dev'
    output = run("git symbolic-ref HEAD")
    #print "output < %s >" % output
    branchName = output.split('/')[2]
    branchNameStripped = branchName.strip()
    return branchNameStripped
