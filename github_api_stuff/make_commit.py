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

## Step ZERO: get a reference
resp = github.repos(owner, repo).git.refs('heads/changes').GET(
    	auth = (user, password))
sha_latest_commit = json.loads(resp._content)['object']['sha']

print sha_latest_commit

## Step ONE: get latest commit at that reference
resp = github.repos(owner, repo).git.commits(sha_latest_commit).GET(
    	auth = (user, password))
sha_base_tree = json.loads(resp._content)['tree']['sha']

print sha_base_tree

## Step TWO: make a new commit, which goes in several substeps

## Step A: update the tree
filename = "Aitken, Alexander C..tex"
encoded_filename=urllib.parse.quote(filename)

data={'message':'Adding "'+text+'".',
      'committer':{'name':'Joe Corneli',
                   'email':'holtzermann17@gmail.com'},
      'base_tree':sha_base_tree,
      'branch':'changes'
      'path':'tex_files/'+encoded_filename,
      'content':base64.b64encode("Hello github")}

resp = github.repos(owner, repo).git.trees.POST(
    auth=(user, password),
    headers = {'Content-type': 'application/json'},
    data=json.dumps(data))

pprint(resp._content)
sha_new_tree = json.loads(resp._content)['sha']

## Step B: 
data={'parents':[sha_latest_commit],
      'tree':sha_new_tree,
      'branch':'changes'}

resp = github.repos(owner, repo).git.commits.PUT(
    auth=(user, password),
    headers = {'Content-type': 'application/json'},
    data=json.dumps(data))

pprint(resp._content)
sha_new_commit = json.loads(resp._content)['sha']

## Step C: 
data={'sha':sha_new_commit,
      'force':True}

resp = github.repos(owner, repo).git.refs('heads/changes').PUT(
    auth=(user, password),
    headers = {'Content-type': 'application/json'},
    data=json.dumps(data))

pprint(resp._content)
