#!/usr/bin/env python
import sys

from jiraFunc import *
from git_util import *
from cookies import *

def printUsage():
    print "Usage: git jira [operation [args]]"
    print "       git jira [describe [branch]]"
    print "Valid operations: %s" % operations.keys()

if(len(sys.argv) < 2):
    printUsage()
    sys.exit(1)

operation = sys.argv[1]

#print "Argument is %s " % operation

def stuff():
    jiraProject = getJiraProjectName()
    print "jira name %s" % jiraProject

    data = loadIssues(jiraProject)

    issue = selectIssue(data['issues'])
    detailedInfo = getIssueInfo(issue['key'])
    prettyPrintJson(detailedInfo)
    print "You want to start",
    #simplePrintIssue(detailedInfo)
    #for issue in data['issues']:
    #    print issue['key']

def opDescribe(argv):
    branchName = None
    if(len(argv) == 1):
        branchName = argv[0]
    else:
        branchName = getBranchName()
    #print "branch name is %s" % branchName
    cookie = cookieHandler()
    try:
        describeBranch(branchName)
    except KeyError as inst:
        #TODO: Shouldn't be KeyError for older version of Jira
        if(inst.args[0] == "Missing Issue"):
            print "Missing issue, so no description for %s" % branchName
        else:
            raise
    except cookie.HTTPError as inst:
        print "Unable to find issue %s (%s)" % (branchName, inst)

def userChooseIssue():
    '''User operation to list the jira issues for the current project'''
    jiraProject = getJiraProjectName()
    data = loadIssues(jiraProject)

    issueData = selectIssue(data['issues'])
    issueName = issueData['key']
    issue = jiraObj(issueName)
    return issue

def opList(argv):
    '''List all the open issues in the current project'''
    jiraProject = getJiraProjectName()
    data = loadIssues(jiraProject)
    print "Open issues:"
    listIssues(data['issues'])

def opHelp(argv):
    printUsage()

def opStart(argv):
    if(len(argv) == 1):
        print "Checking out %s" % argv[0]
        issueName = argv[0]
    else:
        issue = userChooseIssue()
        issueName = issue.name

    print "Starting %s" % issueName
    print "Checking out branch %s" % issueName
    print "Note: Starting the actual jira issue not yet supported"
    createBranch(issueName)
    checkoutBranch(issueName)



def opFeature():
    print "nothing"

def opCreate(argv):
    print "nothing"

def opLogin(argv):
    # Does the equivalent of this curl command
    # curl -c cookie_jar -H "Content-Type: application/json" -d '{"username" : "jaxelson", "password" : "hunter2"}' http://localhost:8080/rest/auth/latest/session
    username = getGitValue('username')
    password = getGitValue('password')
    loginUrl = 'http://localhost:8080/rest/auth/latest/session'
    txdata = '{"username" : "' + username +'", "password" : "'+ password +'"}'
    txheaders =  {'Content-Type' : 'application/json'}
    cookie = cookieHandler()
    req = cookie.Request(loginUrl, txdata, txheaders)            # create a request object
    handle = cookie.urlopen(req)                               # and open it to return a handle on the url
    print handle.read()
    cookie.saveCookies()

def opInit(argv):
    setGitValue('username', 'jaxelson')
    setGitValue('password', 'hunter2')
    loginUrl = 'http://localhost:8080/rest/auth/latest/session'
    cookie = cookieHandler()
    import urllib2
    pass


operations = {
        "describe": opDescribe,
        "feature": opFeature,
        "create": opCreate,
        "list": opList,
        "help": opHelp,
        "start": opStart,
        "login": opLogin,
        "init": opInit,
        "-h": opHelp,
        "--help": opHelp,
        }

try:
    #print "operation is %s " % operation
    operations[operation](sys.argv[2:])
except KeyError:
    print "Sorry, %s is not a valid operation" % operation
    print "Valid operations: %s" % operations.keys()
    print "Try running with -h for help"
    sys.exit(1)

