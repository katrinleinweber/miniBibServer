from hammock import Hammock as Github
import json
import urllib
import sys
import base64
from pprint import pprint

github = Github('https://api.github.com')
owner = 'maddyloo'
repo = 'BibProject'
path = 'tex_files/Aitken%2C%20Alexander%20C..tex'
password = ''  #BibPoject token
#Aitken%2C Alexander C..tex

#GET /repos/:owner/:repo/contents/:path
resp = github.repos(owner, repo).contents(path).GET(
	auth = (owner, password),
	headers = {'Content-type': 'textfile'})
	#data = json.dumps(data))

#j = json.loads(resp.text)
j = resp.json()
print(base64.b64decode(j['content']))
#pprint(resp.content)
