#!/usr/bin/env python
import httplib
import urllib
import json
from subprocess import call
from subprocess import Popen
from subprocess import PIPE

from util import *
from git_util import *
from cookies import *
from connection import *

# Targetting jira version Atlassian JIRA (v4.3.3#617-r149616)

class jiraObj:
    def __init__(self,issue):
        #print "creating jiraObj for %s" % issue
        self.data = getIssueInfo(issue)
        if(self.data.has_key('errorMessages')):
            print "Warning: This issue doesn't exist: %s" % issue
            raise Exception("Missing Issue")
        self.name = self.data['key']
        try:
            self.description = self.data['fields']['description']['value']
        except KeyError:
            self.description = None
        self.summary = self.data['fields']['summary']['value']
        self.status = self.data['fields']['status']['value']['name']

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
        print "Status: %s" % self.status
        print "Jira URL: http://" + jiraUrl + "/browse/" + self.name


# Settings
jiraApi = '/rest/api/2.0.alpha1'
headers = {'Content-type': 'application/json','Accept': 'application/json'}

def describeBranch(branch):
    #print "Describing branch %s" % branch
    obj = jiraObj(branch)
    #obj.printData()
    obj.printDetails()

def getJiraProjectName():
    '''Gets the name of the JIRA project for this repo (prompting the user if necessary)'''
    jiraName = getGitValue('jiraname')
    if(jiraName == ''):
        jiraName = getJiraProjectFromUser()
        setGitValue('jiraname', jiraName)

    return jiraName

def getJiraProjectFromUser(con):
    '''Asks the user to identify the JIRA project they are currently working on by querying the JIRA server for the list of projects and displaying them to the user
    param: con connection to jira
    '''
    cookie = con.getCookie()
    con.ensureLogin()
    jiraProjects = ''
    try:
        jiraProjects = getJiraProjects(con)
    except cookie.HTTPError as inst:
        print "Error: new http error in try error %s" % inst
        return
    print jiraProjects
    #TODO: Clean up output
    print "What JIRA project are you working on (look in the key field)?"
    print "JIRA project key:",
    selection = raw_input()
    return selection

def getJiraUrlFromUser():
    print "Please type your jira url (e.g.: nihoa): "
    #TODO: Support parsing from browser login
    selection = raw_input()
    return selection


def getJiraProjects(connection):
    '''
    Gets the jira projects available to the currently logged in user.
    Example below:
    [{"self":"http://localhost:8080/rest/api/2.0.alpha1/project/HICAP","key":"HICAP","name":"HI Capacity","roles":{}},{"self":"http://localhost:8080/rest/api/2.0.alpha1/project/CC","key":"CC","name":"Test (cc)","roles":{}}]

    param: connection the jira connection object to use
    '''
    url = getJiraApiUrl() + '/project'

    #print "url is < %s >" % url
    #TODO: This might cause a cookie.HTTPError with code 401
    handle = connection.getPage(url)
    jiraProjects = handle.read()
    return jiraProjects


def getJiraApiUrl():
    jiraUrl = getGitValue('url')
    url = 'http://' + jiraUrl + jiraApi
    #print "returning jira api url: %s" % url
    return url

def getIssueInfo(issue):
    #print "Getting info for Jira issue %s" % issue
    endpoint = jiraApi + '/issue/' + issue

    jiraUrl = getGitValue('url')
    url = 'http://' +jiraUrl + endpoint
    con = connection()
    handle = con.getPage(url)
    data = handle.read()

    loaded = json.loads(data)
    return loaded


def loadMyIssues(jiraProject):
    '''Load a list of open issues from JIRA'''
    resolution = 'unresolved'
    query = 'project=%(project)s AND resolution=%(resolution)s AND assignee = currentUser()' % {'project':jiraProject, 'resolution': resolution}

    endpoint = jiraApi + '/search'

    params = urllib.urlencode({'jql': query})

    con = connection()

    jiraUrl = getGitValue('url')
    url = 'http://' + jiraUrl + endpoint+"?" +params
    #req = cookie.Request(url, None, headers)
    #TODO: Might cause a 401 error
    handle = con.getPage(url)
    data = handle.read()

    loaded = json.loads(data)
    #print loaded
    return loaded

def loadIssues(jiraProject):
    '''Load a list of open issues from JIRA'''
    resolution = 'unresolved'
    query = 'project=' + jiraProject + ' AND resolution=' + resolution
    endpoint = jiraApi + '/search'

    params = urllib.urlencode({'jql': query})

    con = connection()

    jiraUrl = getGitValue('url')
    url = 'http://' + jiraUrl + endpoint+"?" +params
    #req = cookie.Request(url, None, headers)
    #TODO: Might cause a 401 error
    handle = con.getPage(url)
    data = handle.read()

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
    print "Select from the issues below:"
    listIssues(issues)
    print "Issue number:",
    selection = raw_input()
    print
    return getIssueDescription(issues, selection)

def getIssueDescription(issues, issueToGet):
    '''Get an issue description from a list of issues'''
    for issue in issues:
        if issueToGet in issue['key']:
            return issue

def checkInitialized():
    '''
    Checks if the current repository is initialized for git jira, if it
    isn't then give error and exit
    '''
    # Need to check for jiraname, username, and url
    for name in ['jiraname', 'username', 'url']:
        value = getGitValue(name)
        if(value == ''):
            print "Missing value for %s!" % name
            print "Please run 'git jira init' to fix"
            sys.exit(1)

def prettyPrintJson(jsonText):
    import json
    print json.dumps(jsonText, sort_keys=True, indent=4)
