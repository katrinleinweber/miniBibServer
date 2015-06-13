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
password = '8befeade219b038b9189a153fdb282cefa04c5b1' #Github token goes here

filename = "Aitken, Alexander C..tex"

data = {"title": "Update to " + filename,
        "body": "Please pull this in!",
        "head": "changes",
        "base": "master"}

resp = github.repos(owner, repo).pulls.POST(
    	auth = (user, password),
        headers = {'Content-type': 'application/json'},
        data=json.dumps(data))

pprint(resp._content)
