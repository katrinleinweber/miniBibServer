# -*- coding: utf-8; -*-

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
# Maps to AitkenAlexanderC as a "canonical name"
basename = re.sub('[ ,.]', '', filename.split(".")[0])

## Step ZERO: get a reference
resp = github.repos(owner, repo).git.refs('heads/master').GET(
    	auth = (user, password))
sha_latest_commit = json.loads(resp._content)['object']['sha']

## Step ONE: create the branch derived from that reference
data={"ref": "refs/heads/"+basename,
      "sha": sha_latest_commit}

resp = github.repos(owner, repo).git.refs.POST(
    	auth = (user, password),
        headers = {'Content-type': 'application/json'},
        data=json.dumps(data))

pprint(resp._content)


