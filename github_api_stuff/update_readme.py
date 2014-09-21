from hammock import Hammock as Github
import json
import base64
from pprint import pprint

# Let's create the first chain of hammock using base api url
github = Github('https://api.github.com')

user = 'holtzermann17'
# In the future this will be running on a server
# somewhere, so password can just be hard coded
password = raw_input("Enter your github password: ")
repo = 'py-blot'

# The most interesting things for us are in this part of the API
# https://developer.github.com/v3/repos/contents/

# get the contents of a given file, the README in this case
resp = github.repos(user, repo).contents.GET('README.md')

# examine the file we retrieved,
# here's how to have a look at everything:
#pprint(vars(resp))
# And from that, the most interesting part(s) can be extracted:
text = base64.b64decode(json.loads(resp._content)['content'])
# (we will need the sha later)
sha = json.loads(resp._content)['sha']

print text

# Now to further explore the API, let's loop back and
# update the file.  Let's prompt the user to add
# some text to the file.

delta = raw_input("Add text: ")

newtext = ''.join([text, '\n', delta]) 

newcontent = base64.b64encode(newtext)
#message = base64.b64encode()

data={'message':'Adding "'+text+'".',
      'committer':{'name':'Joe Corneli',
                   'email':'holtzermann17@gmail.com'},
      'content':newcontent,
      'sha':sha,
      'branch':'master'}

# Forming the correct URL (by following the instructions from Hammock docs!)
# In particular, we need to specify the :path as part of the url, whereas
# other arguments are passed along as a JSON body
resptwo = github.repos(user, repo).contents('README.md').PUT(
    auth=(user, password),
    headers = {'Content-type': 'application/json'},
    data=json.dumps(data))

pprint(vars(resptwo))

# Here's how to do something similar with curl:

# curl -i -X PUT -H 'Authorization: <token>' -d '{"path": "test4.txt", "message": "Initial Test", "committer": {"name": "Joe Corneli", "email": "holtzermann17@gmail.com"}, "content": "bXkgbmV3IGZpbGUgY29udGVudHM=", "branch": "master"}' https://api.github.com/repos/holtzermann17/py-blot/contents/test4.txt
