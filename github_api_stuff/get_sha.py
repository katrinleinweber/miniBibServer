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
sha_latest_commit = json.loads(resp._content)['object']['sha']

print sha_latest_commit

## We may also need this other sha?

resp = github.repos(owner, repo).git.commits(sha_latest_commit).GET(
    	auth = (user, password))
sha_base_tree = json.loads(resp._content)['tree']['sha']

print sha_base_tree

