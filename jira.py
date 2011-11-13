#!/usr/bin/env python
import sys

from jiraFunc import *
from git_util import *
from cookies import *

def printUsage():
    print "Usage: git jira [describe [branch]]"
    print "       git jira [list]"

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

def describe(argv):
    branchName = None
    if(len(argv) == 1):
        branchName = argv[0]
    else:
        branchName = getBranchName()
    #print "branch name is %s" % branchName
    try:
        describeBranch(branchName)
    except Exception as inst:
        if(inst.args[0] == "Missing Issue"):
            print "Missing issue, so no description for %s" % branchName
        else:
            raise

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
    gitUsername = getGitValue('username')
    theurl = 'http://localhost:8080/rest/auth/latest/session'
    txdata = '{"username" : "' + gitUsername +'", "password" : "hunter2"}'
    txheaders =  {'Content-Type' : 'application/json'}
    obj = cookieHandler()
    req = obj.Request(theurl, txdata, txheaders)            # create a request object
    handle = obj.urlopen(req)                               # and open it to return a handle on the url
    print "got page!"
    print handle.read()


operations = {
        "describe": describe,
        "feature": opFeature,
        "create": opCreate,
        "list": opList,
        "help": opHelp,
        "start": opStart,
        "login": opLogin,
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

