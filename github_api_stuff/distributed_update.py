# -*- coding: utf-8; -*-

from hammock import Hammock as Github
import json
import urllib
import sys
import base64
import filecmp
import re

# This file will just contain the list of names and URLs of source material.
import ims_sources

from pprint import pprint

## Some assumptions about the layout of things

# Let's assume that a checked out version of the BibProject is available at, for example
# /home/joe/jim/BibProject/

# We'll make a new branch for each commit, so that we can close things out cleanly.

# Here's the basic information for using the Github API:

github = Github('https://api.github.com')
owner = 'maddyloo'
repo = 'BibProject'
user = 'holtzermann17'
password = '8befeade219b038b9189a153fdb282cefa04c5b1' #Github token goes here

## Relevant functions

def make_branch(basename):
    """Just make a new branch with this name."""
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

def make_commit(basename,filename,content):
    """Update filename in the branch basename to hold given content."""

    encoded_filename=urllib.quote(filename)
    path = 'tex_files/'+encoded_filename

    ## Step ONE: get the current file so we can extract its hash
    ## this isn't the "canonical" way to go about making a commit
    ## described variously with five or seven steps, see
    ## make_commit.py for the "right way to do this" (work in progress).
    data={'ref':basename}
    resp = github.repos(owner, repo).contents(path).GET(
        	auth = (user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))
    
    sha = json.loads(resp._content)['sha']
    
    ## Step TWO: add the new content
    data={'message':'Programmatic update to "' + filename + '".',
          'committer':{'name':'Joe Corneli',
                       'email':'holtzermann17@gmail.com'},
          'content':base64.b64encode(content),
          'sha':sha,
          'branch':basename}
    
    # Forming the correct URL (per the instructions from the Hammock docs!)
    # In particular, we need to specify the :path as part of the url, whereas
    # other arguments are passed along as a JSON body
    resp = github.repos(owner, repo).contents(path).PUT(
            auth=(user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))

def make_pull_request(filename,basename):
    data = {"title": "Update to " + filename,
            "body": "Please pull this in!",
            "head": basename,
            "base": "master"}
    
    resp = github.repos(owner, repo).pulls.POST(
        	auth = (user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))

## Step 1: download copies of all files in our list

# For this, we need a list.  Let's start with something simple like
# this: The http://... stand for items that are maintained "elsewhere"
# whereas the tex_files/... stand for items that are mantained by IMS
# and presumably stored in the same git repo.

# We can make this an association between (canonical) member names and remote URLs
# (Eventually this will expand to have all of the members on it.)
# And it should probably be stored in a separate file so that it's easier to update.

# We'll do the actual downloading as part of a loop in the next step

## Step 2: compare downloaded files to local copies

def check_local (source):
    """We may eventually do something interesting but for now, just ignore."""
    print(".")

## Continue the script
##  - note, we may want to add some error handling in case the URLs don't load
for item in ims_sources.urllist:
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

        try: 
            content = urllib.urlopen(source).read()
        except urllib2.HTTPError, e:
            # we could do some more sophisticated logging here, and throughout
            print('HTTPError = ' + str(e.code))
        else:
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
                basename = re.sub('[ ,.]', '', person_name)
                make_branch(basename)
                make_commit(basename,new_filename,content)
                # we should probably update the HTML automatically as well, but maybe
                # just what we do about it will depend on what IMS wants...
                # I guess that part can wait until after deploying this version,
                # it's not going to require a major change to the code
                make_pull_request(new_filename,basename)
    
# distributed_update.py ends here
