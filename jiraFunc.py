#!/usr/bin/env python
import httplib
import urllib
import json
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

# Targetting jira version Atlassian JIRA (v4.3.3#617-r149616)

class jiraObj:
    def __init__(self,issue):
        #TODO: Handle when the issue doesn't exist in JIRA
        self.data = getIssueInfo(issue)
        self.name = self.data['key']
        try:
            self.description = self.data['fields']['description']['value']
        except KeyError:
            self.description = None
        self.summary = self.data['fields']['summary']['value']
    def printData(self):
        print "name: %s" % self.name
        print "summary: %s" % self.summary
        print "description: %s" % self.description
        #prettyPrintJson(self.data)

    def simplePrintIssue(self):
        #print detailedIssueInfo['fields']
        #TODO: Print out the summary field (subject)
        print "%(name)s: %(summary)s - %(description)s" % {"name":self.name, "summary":self.summary, "description":self.description}

    def printDetails(self):
        #print detailedIssueInfo['fields']
        #TODO: Print out the summary field (subject)
        print "%(name)s: %(summary)s" % {"name":self.name, "summary":self.summary}
        print
        print self.description


# Settings
jira = 'nihoa'
jiraApi = '/rest/api/2.0.alpha1'
headers = {'Content-type': 'application/json','Accept': 'application/json'}

def run(command):
    #print "running %s " % command
    pipe = Popen(str.split(command), stdout=PIPE, stderr=PIPE)
    output = pipe.stdout.read()
    return output

def describeBranch(branch):
    obj = jiraObj(branch)
    #obj.printData()
    obj.printDetails()

def getJiraProjectName():
    '''Gets the name of the JIRA project for this repo (prompting the user if necessary)'''
    jiraName = run("git config rams.jiraname")
    if(jiraName == ''):
        print "No jira name set, what is the jira name of this repo? "
        selection = raw_input()
        setJiraProjectName(selection)
        jiraName = selection

    return jiraName

def setJiraProjectName(name):
    '''Set the name of the JIRA project for this repo'''
    run("git config rams.jiraname %s" % name)

def getIssueInfo(issue):
    #print "Getting info for Jira issue %s" % issue
    endpoint = jiraApi + '/issue/' + issue

    conn = httplib.HTTPConnection(jira);
    conn.request('GET',url=endpoint,headers=headers)
    response = conn.getresponse()
    data = response.read()

    loaded = json.loads(data)
    return loaded


def loadIssues(jiraProject):
    resolution = 'unresolved'
    query = 'project=' + jiraProject + ' AND resolution=' + resolution
    endpoint = jiraApi + '/search'
    #print "endpoint: %s" % endpoint

    '''Load a list of open issues from JIRA'''
    conn = httplib.HTTPConnection(jira);
    params = urllib.urlencode({'jql': query})
    conn.request('GET',url=endpoint+"?" +params,headers=headers)
    response = conn.getresponse()
    data = response.read()

    loaded = json.loads(data)
    #print loaded
    return loaded

def listIssues(issues):
    '''List the issue number and summary for each issue'''
    for issue in issues:
        issueName = issue['key']
        issueObj = jiraObj(issueName)
        print "    %(name)s: %(summary)s" % {"name":issueObj.name, "summary":issueObj.summary}

def selectIssue(issues):
    '''Prompt the user to select an issue from a list of issues'''
    print "Select an issue:"
    listIssues(issues)
    selection = raw_input()
    return getIssueDescription(issues, selection)

def getIssueDescription(issues, issueToGet):
    '''Get an issue description from a list of issues'''
    for issue in issues:
        if issueToGet in issue['key']:
            return issue

def prettyPrintJson(jsonText):
    import json
    print json.dumps(jsonText, sort_keys=True, indent=4)

def getBranchName():
    '''Return the name of the current branch'''
    #TODO Move into a git.py file
    # Expect output like 'refs/heads/dev'
    output = run("git symbolic-ref HEAD")
    branchName = output.split('/')[2]
    return branchName
