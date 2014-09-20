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
encoded_filename=urllib.quote(filename)
path = 'tex_files/'+encoded_filename

data={'ref':"changes"}

## Step ZERO: get the current file so we can extract its hash
resp = github.repos(owner, repo).contents(path).GET(
    	auth = (user, password),
        headers = {'Content-type': 'application/json'},
        data=json.dumps(data))

sha = json.loads(resp._content)['sha']

## Step ONE: add the new content
data={'message':'Programmatic update to "' + filename + '".',
      'committer':{'name':'Joe Corneli',
                   'email':'holtzermann17@gmail.com'},
      'content':base64.b64encode("Hello github, new content here."),
      'sha':sha,
      'branch':'changes'}

# Forming the correct URL (by following the instructions from Hammock docs!)
# In particular, we need to specify the :path as part of the url, whereas
# other arguments are passed along as a JSON body
resp = github.repos(owner, repo).contents(path).PUT(
        auth=(user, password),
        headers = {'Content-type': 'application/json'},
        data=json.dumps(data))

pprint(resp._content)
