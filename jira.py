#!/usr/bin/env python
import sys
import getpass

from jiraFunc import *
from git_util import *
from cookies import *
from connection import *

def printUsage():
    print "Usage: git jira [operation [args]]"
    print "       git jira [describe [branch]]"
    print "Valid operations: %s" % operations.keys()

if(len(sys.argv) < 2):
    printUsage()
    sys.exit(1)

operation = sys.argv[1]

#print "Argument is %s " % operation

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
    con = connection()
    if (con.checkLogin()):
        print "Already logged in"
        return
    con.ensureLogin()

def opInit(argv):
    setGitValue('password', 'hunter2')
    url = getJiraUrlFromUser()
    setGitValue('url', url)

    print "Please type your username: "
    username = raw_input()
    setGitValue('username', username)

    print "Do you want to store your password unencrypted in .git/config? (y/n)"
    selection = raw_input()
    if (selection == 'y'):
        password = getpass.getpass()
        setGitValue('password', password)

    con = connection()
    jiraProject = getJiraProjectFromUser(con)
    setGitValue('jiraname', jiraProject)

    print
    print "git-jira initialized successfully"



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

