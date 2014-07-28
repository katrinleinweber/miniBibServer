#This Python file bibtex.py uses the following encoding: utf-8

## BibServer BibTeX Parser
## License:  http://opensource.org/licenses/BSD-2-Clause
#Copyright (c) 2014, Jim Pitman
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
# disclaimer in the documentation and/or other materials provided with the distribution.
#

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
#IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EX
#OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 

#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
#EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Note. This code is extracted from the original BibServer BibTeX parser developed by Jim Pitman in 2003. This parser and associated html displays
# have been operating since then as a webservice at http://bibserver.berkeley.edu/cgi-bin/bibs7
# Developments of this code are also available at https://github.com/okfn/bibserver under the MIT License, Copyright (c) 2010 Open Knowledge Foundation

from string import replace
import cgi,os, re, string, urllib, string, copy, sys, time, glob, StringIO

import accents

#### TOOLS FOR HANDLING NAME STRINGS  #####

def first_last(namestring):
	## (firstname, lastname) = first_last(namestring)
	namestring = string.strip(namestring)
	if string.find( namestring, ',') >= 0: 
		namesplit  =  string.split(namestring, ',',1)
		return (string.strip(namesplit[1]),  string.strip(namesplit[0]))
	else:
		try:
			if string.find(namestring,' Le ') >= 0:
				namestringsplit  =  string.split(namestring, 'Le ',1)
				lastname = 'Le ' + namestringsplit[1]
				firstnames = namestringsplit[0]
			elif string.find(namestring,' van ') >= 0:
				namestringsplit  =  string.split(namestring, 'van ',1)
				lastname = 'van ' + namestringsplit[1]
				firstnames = namestringsplit[0]
			else:
				namestringsplit  =  string.split(namestring)
				lastname = namestringsplit[ len(namestringsplit) - 1]
				firstnames = ''
				for frag in namestringsplit:
					if frag != lastname:	
						firstnames = firstnames + ' ' + frag
			return (string.strip(firstnames), string.strip(lastname))
		except IndexError:
			#return (namestring,namestring)
			return ('','')
			#return ('Unable_to_parse_name_string_for_first_name', 'Unable_to_parse_name_string_for_last_name')


def last_name(namestring):
	(first, last) = first_last(namestring)
	return last 

def first_name(namestring):
	(first, last) = first_last(namestring)
	return first 

def first_initial (namestring):
	(first, last) = first_last(namestring)
	try:
		return first[0] 
	except IndexError: return ''

def initials(namestring):
	(first, last) = first_last(namestring)
	ss = string.split(first)
	inits = ''
	for s in ss:
		try:
			inits += ' ' + s[0]
		except: IndexError
	return inits

def last_name_first(namestring):
	(first, last) = first_last(namestring)
	if string.strip(last + first) != '': return last + ', ' + first
	else: return ''

def first_name_first(namestring):
	(first, last) = first_last(namestring)
	return first + ' ' + last

def author_ls(author):
	author = string.replace(author,'\n',' ')
	ss = string.split(author,' and ')
	au_ls = []
	for  a in string.split(author,' and '):
		au_ls += [a]
	return au_ls
###########################################################################################

"""Functions to read a BibTeX string and convert it to a list of dictionaries.
"""


string_dict = {}
"""Dictionary for string definitions"""
# to do:  could also handle preamble definitions. 

def up(instring):
	return string.upper(string.strip(instring))
	"""Capitalize and string.strip"""

def lo(instring):
	return string.lower(string.strip(instring))
	"""Uncapitalize and string.strip"""

def strip_quotes(instring):
	"""Strip double quotes enclosing string"""
	instring = string.strip(instring)
	if instring[0] == '"' and instring[-1] == '"':
		return instring[1:-1]
	else: return instring

def strip_braces(instring):
	"""Strip braces enclosing string"""
	instring = string.strip(instring)
	if instring[0] == '{' and instring[-1] == '}':
		return instring[1:-1]
	else: return instring

def test(instring):  
	"""Test to check if instring is well-formed value of a bibtex field:
	returns 
	( number of double quotes mod 2, number of left braces - number right braces )
	"""
	instring = string.replace(instring,'\\"','')
	quote_count = string.count(instring,'"')
	lb_count = string.count(instring,'{')
	rb_count = string.count(instring,'}')
	return (divmod(quote_count , 2)[1] ,lb_count - rb_count)

def string_subst(instring):
	""" Substitute string definitions """
	for k in string_dict.keys():
		instring = string.replace(instring,k,string_dict[k])
	return instring

keys_dict = {}
""" Dictionary of keys and their substitutions """
keys_dict['keyw'] = 'subjects'
keys_dict['authors'] = 'author'
keys_dict['bibtex'] = 'url_bib'

def add_key(key):
	""" Add NOT upper-cased key to keys dictionary """
	key = key.strip()
	if key in keys_dict.keys():
		return keys_dict[key]
	else: return key
		
def add_val(instring):
	""" Clean instring before adding to dictionary """
	if instring[-1] == ',': val = string.strip(instring)[:-1]  ###delete trailing ','
	else: val = instring
	val = strip_braces(val)
	val = strip_quotes(val)
	val = strip_braces(val)
	val = string_subst(val)
	return val

def read_bibitem(item):     ### returns a python dict
		d = {} 
		type_rest = string.split(item, '{' ,1)
		d['bibtype'] = type_rest[0]
		try:
			rest = type_rest[1]
		except IndexError:
			d['ERROR'] = 'IndexError: nothing after first { in @' + item
			rest = ''
		if d['bibtype'] == 'STRING':
		###### Example:   @string{AnnAP = "Ann. Appl. Probab."}
			try:
				key_val = string.split(rest,'=')
				key = string.strip(key_val[0])
				val = string.strip(key_val[1])
				val = string.strip(val[:-1])   ## strip the trailing '}'
				val = val[1:-1]                ## strip the outer quotes 
				string_dict[key] = val
				#print 'string_dict[', key, '] = ', val
	
			except IndexError:
				d['ERROR'] = 'IndexError: can\'t parse string definition in @' + item
				rest = ''
			
		else:
			comma_split = string.split(rest,',',1)
			d['citekey'] = string.strip(comma_split[0])
			# d['BIBTEX'] = '@' + item
			try:
				rest = comma_split[1]
			except IndexError:
				d['ERROR'] = 'IndexError: nothing after first comma in @' + item
				rest = ''
			
			count = 0
			current_field = ''
			while count <= 100:   ### just a safey net to avoid infinite looping if code breaks
				count = count + 1
				comma_split = string.split(rest,',',1)
				this_frag = comma_split[0]
				current_field = current_field + this_frag + ','
				(quote_count,br_count) = test(current_field)
				if quote_count == 0 and br_count == 0:
					key_val = string.split(current_field,'=',1)
					key = key_val[0]
					try:
						d[add_key(key)] = add_val( key_val[1])
					except IndexError:
						d[add_key(key)] = ''
					current_field = ''
				elif quote_count == 0 and br_count < 0:    ###end of bibtex record
					key_val = string.split(current_field,'=',1)
					key = key_val[0]
					try:
						rest = comma_split[1]
					except IndexError:
						rest = ''
					try:
						val_comments  = string.split(key_val[1],'}')
						val = val_comments[0] 
						(quote_count,br_count) = test(val)
						if br_count == 1: val = val + '}'  
						else: val = val + ','  ## add comma to match format
						#### problem is record can end with  either e.g.
						#### year = 1997}
						#### year = {1997}}
						if string.find(key,'}') < 0:
							d[add_key(key)] = add_val( val)
						#d['ERROR'] = str( br_count )
						## putting error messages into d['ERROR'] is a good
						## trick for debugging
						try:
							comments = val_comments[1][:-1]
							comments = string.strip(comments)
							if comments != '':
								d['BETWEEN_ENTRIES'] = add_val(comments + ',') + add_val(rest)
						except: IndexError
					except: IndexError
					current_field = ''
					break
				try:
					rest = comma_split[1]
				except IndexError:
					key_val = string.split(current_field,'=',1)
					key = add_key( key_val[0] )
					if key != '':
						try:
							d[key] = add_val( key_val[1])
						except IndexError:
							d[key] = ''
					break
		### impute year from Davis Fron to arxiv output:
		if d.has_key('EPRINT') and not d.has_key('YEAR'): 
			yy = '????'
			ss = string.split(d['EPRINT'],'/')
			if len(ss) == 2: yy = ss[1][0:2]
			if yy[0] in ['0']: d['YEAR'] = '20' + yy   ### year 2010 problem!!
			elif yy[0] in ['9']: d['YEAR'] = '19' + yy
		return d

def read_bibstring(instring):  ###parses a bibtex string into a list of dictionaries
    """ Main function 
    Input is a string, interpreted as bibtex, output is a list of dictionaries.
    All keys are regularized to upper case, and according to substitutions in the keys_dict"""
    #for line in string.split(instring,'\n'):
    #	if string.find(line,'--BREAK--') >= 0:    
    #		break
    #	else: lines = lines + [string.strip(line)]
    try: instring =  unicode(instring,'utf-8')
    except: pass
    instring = '\n' + instring
    items = instring.split('\n@')
    return [ read_bibitem(item) for item in items[1:] ]

	
def dict2bibtex(d):
	""" Simple function to return a bibtex entry from a python dictionary """
	outstring =  '@' + d.get('TYPE','UNKNOWN') + '{' + d.get('KEY','') + ',\n'
	kill_keys = ['TYPE','KEY','ORDER']
	top_keys = ['AUTHOR','TITLE','YEAR']
	top_items = []
	rest_items = []
	for k in d.keys():
		if k in top_keys:
			top_items = top_items + [ ( k , d[k] )]
		elif not k in kill_keys:
			rest_items = rest_items + [ ( k , d[k] )]
	rest_items.sort()
	for k in top_items + rest_items:
		outstring = outstring + '\t' + k[0] + ' = {' + k[1] + '},\n'
	outstring = outstring +  '}\n\n'
	return outstring

def clean(txt):
    #txt = ' '.join( txt.split() )     ## bad for bibtex
    try: return accents.tex2utf8(txt)
    except: return txt

def clean_dict(d):
    if d.has_key('BIBTYPE') and d.has_key('CITEKEY'):
        e = {}
        for k in d.keys(): 
            e[k.lower()] = d[k]
        e['id'] = e['citekey']
        del e['citekey']
        for k in e.keys():
            if not k == 'bibtex':
                e[k] = clean(e[k])
        return e
    else: return d

def read_bibstring_cleaned(instring):  
    dls = read_bibstring(instring)
    return [ clean_dict(d) for d in dls ] 


def bibtex2d (b):     
    """ convert bibtex string for a single item to a dictionary. Cleans up read_bibstring for a single item """
    dls = read_bibstring(b)
    if not dls: return {}
    d = dls[-1]  ## to avoid accent preambles
    e = {}
    for k in d.keys():
        e[k.lower()] = clean(d[k])
    e['bibtype'] = e['bibtype'].lower()
    e['id'] = e['citekey']
    del e['citekey']
    return e
