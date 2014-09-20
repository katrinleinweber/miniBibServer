# -*- coding: utf-8; -*-

from hammock import Hammock as Github
import json
import urllib
import sys
import base64
import filecmp

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
    """We may eventually do something a bit more interesting."""
    print "Found local source!"

## Continue the script - may want to add some error handling in case the URLs don't load
## 
for item in sources:
    person_name=item[0]
    print "person name: " + person_name
    source=item[1]
    # Maybe the only thing to do in this case is produce some new HTML,
    # assuming we keep "staged" and "working" copies separate.  But as
    # a first step, let's assume there's nothing to do in this case, and
    # we just need to process the upstream files.
    if (source[:9] == "tex_files"):
        upstream_filename = urllib.unquote(source.rsplit("/",1)[1])
        print "filename:" + upstream_filename
        check_local(source)
    else:
        upstream_filename = urllib.unquote(source.rsplit("/",1)[1])    
        content = urllib.urlopen(source).read()
        local_filename = "/home/joe/jim/BibProject/tex_files/" + person_name + ".tex"
        new_filename = person_name + ".tex"
        with open(new_filename, "w") as new_file:
            # the comparison won't work unless the file has been written and closed!
            new_file.write(content)
            new_file.close()
        # val will be True if the files are the same, and False if they differ.
        val = filecmp.cmp(person_name + ".tex", local_filename)
        print "Val is: " + str(val)
        print "local filename:" + local_filename
        print "new filename:" + new_filename
        print "content:" + content[:36]
        if (not(val)):
            commit_and_make_pull_request(new_filename)

## Step 3: If different, make a commit and submit a pull request
def commit_and_make_pull_request(filename):
    ## Basic definitions
    github = Github('https://api.github.com')
    owner = 'maddyloo'
    repo = 'miniBibServer'
    
    ## A: Get the SHA of the most recent commit to this branch
    resp = github.repos(owner, repo).git.refs.heads.GET('changes')
    sha = json.loads(resp._content)['sha']

    with open( filename, "rb") as text_file:
    	encoded_string = base64.b64encode(text_file.read())
    
    data = {'message':'Adding "'+filename+'".',
          'committer':{'name':'Joe Corneli',
                       'email':'holtzermann17@gmail.com'},
          'content':encoded_string,
          'branch':'master'}
    
    github = Github('https://api.github.com')

    path = 'test_LaTeXML/corneli-citations.bib'
    user = 'holtzermann17'
    password = '8befeade219b038b9189a153fdb282cefa04c5b1' # Github token

    resp = github.repos(user, repo).contents(filename).PUT(
	auth = (user, password),
	headers = {'Content-type': 'textfile'},
	data = json.dumps(data))
    
    #j = json.loads(resp.text)
    j = resp.json()
    print(base64.b64decode(j['content']))
    #pprint(resp['_content'])


sys.exit("Stop here for now")
