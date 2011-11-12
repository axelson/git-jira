#!/usr/bin/env python
import sys

from jiraFunc import *

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
    describeBranch(branchName)

def opChoose():
    '''User operation to list the jira issues for the current project'''
    jiraProject = getJiraProjectName()
    data = loadIssues(jiraProject)

    issueData = selectIssue(data['issues'])
    issueName = issueData['key']
    issue = issueObj(issueName)

    print "You want to start",
    issue.simplePrintIssue()

def opList(argv):
    '''List all the open issues in the current project'''
    jiraProject = getJiraProjectName()
    data = loadIssues(jiraProject)
    listIssues(data['issues'])

def opHelp(argv):
    printUsage()


def opFeature():
    print "nothing"

def opCreate():
    print "nothing"

operations = {
        "describe": describe,
        "feature": opFeature,
        "create": opCreate,
        "list": opList,
        "help": opHelp,
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

