# -*- coding: utf-8; -*-

from hammock import Hammock as Github
import json
import urllib
import sys
import base64
from pprint import pprint

## Some assumptions about the layout of things

# Let's assume that a checked out version of the BibProject is available at, for example
# /home/joe/jim/BibProject/

# Let's assume that the program has its own branch of the Git
# repository where it makes commits, e.g. an "updates" branch


## Step 1: download copies of all files in our list

# For this, we need a list.  Let's start with something simple like
# this: The http://... stand for items that are maintained "elsewhere"
# whereas the tex_files/... stand for items that are mantained by IMS
# and presumably stored in the same git repo.

# We can make this an association between (canonical) member names and remote URLs
# (Eventually this will expand to have all of the members on it.)

sources = [["Aitken, Alexander C.", "http://metameso.org/~joe/aitken.tex"],
           ["Birnbaum, Z. William", "http://metameso.org/~joe/birnbaum.tex"],
           ["Carver, Harry C.", "tex_files/Carver%2C%20Harry%20C..tex"],
           ["Dugué, Daniel", "tex_files/Dugu%C3%A9%2C%20Daniel.tex"]]

# We'll do the actual downloading as part of a loop in the next step

## Step 2: compare downloaded files to local copies

def check_local (source):
    print "Found local source!"

for item in sources:
    name=item[0]
    print "name: " + urllib.unquote(name)
    source=item[1]
    # Maybe the only thing to do in this case is produce some new HTML,
    # assuming we keep "staged" and "working" copies separate.  But as
    # a first step, let's assume there's nothing to do in this case, and
    # we just need to process the upstream files.
    if (source[:9] == "tex_files"):
        filename = urllib.unquote(source.rsplit("/",1)[1])
        print "filename:" + filename
        check_local(source)
    else:
        filename = urllib.unquote(source.rsplit("/",1)[1])
        content = urllib.urlopen(source).read()
        print "filename:" + filename
        print "content:" + content[:36]
        # Now that we have the content we need a good way to make the comparison

# set(fileA.readlines()).difference(set(fileB.readlines()))

sys.exit("Stop here for now")


## Step 3: If different, submit pull request

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
