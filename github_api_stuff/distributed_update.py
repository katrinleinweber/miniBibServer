from hammock import Hammock as Github
import json
import urllib
import sys
import base64
from pprint import pprint

'''
Step 1: download copies of all files in our list

Step 2: compared dowloaded files to local copies

Step 3: IF different, submit pull request

github = Github('https://api.github.com')
owner = 'maddyloo'
repo = 'miniBibServer'
path = 'test_LaTeXML/corneli-citations.bib'
#GET /repos/:owner/:repo/contents/:path
resp = github.repos(owner, repo).contents(path).GET(
	#auth = (user, password),
	headers = {'Content-type': 'textfile'})
	#data = json.dumps(data))

#j = json.loads(resp.text)
j = resp.json()
print(base64.b64decode(j['content']))
#pprint(resp['_content'])