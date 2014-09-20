from hammock import Hammock as Github
import json
import urllib
import sys
import base64
import filecmp

from pprint import pprint

github = Github('https://api.github.com')
owner = 'maddyloo'
repo = 'BibProject'
user = 'holtzermann17'
password = '' #Github token goes here

resp = github.repos(owner, repo).git.refs('heads/changes').GET(
    	auth = (user, password))
#sha = json.loads(resp._content)['sha']

pprint(json.loads(resp._content)['object']['sha'])
