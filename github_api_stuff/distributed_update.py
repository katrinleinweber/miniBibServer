# -*- coding: utf-8; -*-

from hammock import Hammock as Github
import json
import urllib2
import os
import sys
import base64
import filecmp
import re

#__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#lib_path = os.path.abspath('/bibserver/ims_legacy/BibProject/')
#sys.path.append(lib_path)

# This file will just contain the list of names and URLs of source material.
# import ims_sources

from pprint import pprint

## Some assumptions about the layout of things

# Let's assume that a checked out version of the BibProject is available at, for example
# /bibserver/ims_legacy/BibProject/

# We'll make a new branch for each commit, so that we can close things out cleanly.

# Here's the basic information for using the Github API:

github = Github('https://api.github.com')
owner = 'BioBib'
repo = 'BibProject'
user = 'holtzermann17'
password = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Github token goes here

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

def make_commit(refname,directory,filename,content):
    """Update filename in the branch refname to hold given content."""

    encoded_filename=urllib2.quote(filename)
    path = directory+"/"+encoded_filename

    #print refname
    #print path

    ## Step ONE: get the current file so we can extract its hash.
    ## This isn't the "canonical" way to go about making a commit
    ## described variously with five or seven steps, see
    ## make_commit.py for the "right way to do this" (work in progress).
    data={'ref':refname}
    resp = github.repos(owner, repo).contents(path).GET(
        	auth = (user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))
    
    #pprint(json.loads(resp._content))

    sha = json.loads(resp._content)['sha']
    
    ## Step TWO: add the new content
    data={'message':'Programmatic update to "' + filename + '".',
          'committer':{'name':'Joe Corneli',
                       'email':'holtzermann17@gmail.com'},
          'content':base64.b64encode(content),
          'sha':sha,
          'branch':refname}
    
    # Forming the correct URL (per the instructions from the Hammock docs!)
    # In particular, we need to specify the :path as part of the url, whereas
    # other arguments are passed along as a JSON body
    resp = github.repos(owner, repo).contents(path).PUT(
            auth=(user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))


def make_pull_request(descriptor,basename):
    data = {"title": "Update to " + descriptor,
            "body": "Please pull this in!",
            "head": basename,
            "base": "master"}
    
    resp = github.repos(owner, repo).pulls.POST(
        	auth = (user, password),
            headers = {'Content-type': 'application/json'},
            data=json.dumps(data))

    
# distributed_update.py ends here
