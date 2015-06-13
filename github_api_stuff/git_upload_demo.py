from hammock import Hammock as Github
import json
import urllib
import sys
import base64
from pprint import pprint

#upload file to github
'''
with open( filename, "rb") as text_file:
	encoded_string = base64.b64encode(text_file.read())

data = {'message':'Adding "'+filename+'".',
      'committer':{'name':'Madeleine Corneli',
                   'email':'mlc299@cornell.edu'},
      'content':encoded_string,
      'branch':'master'}

github = Github('https://api.github.com')
user = 'maddyloo'
password = raw_input("Github password:")
repo = 'miniBibServer'
resp = github.repos(user, repo).contents(filename).PUT(
	auth = (user, password),
	headers = {'Content-type': 'textfile'},
	data = json.dumps(data))

pprint (vars(resp))
'''
#edit to test git :/

#data = {'owner':'maddyloo',
#	#might need full path: 
#	'path':'/master/test_LaTeXML/corneli-citations.bib',
#	'repo':'miniBibServer'}

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