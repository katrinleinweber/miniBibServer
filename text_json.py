import os
import json 
import glob
import time
import datetime
time_stamp = unicode( datetime.datetime.now().isoformat().split('.')[0], 'utf-8')   
import random
import latex_accents
import re
import bibtex
import display_function

import aitken_sample_d
import pprint

pp = pprint.PrettyPrinter(indent=4)

def make_all():
    #runs publish_json on all .tex files in a directory
    rootdir = "C:/Users/mnhockeygirl/Desktop/me/json_files"
    origindir = "/tex_files"
    for files in os.walk(origindir):
        for file in files:
            print file
    print "done!"

def publish_json(name):
    filename = name + ".tex"
    newfile = name + ".json"
    content = {}
    #open .tex file
    f = open(filename)
    n = open(newfile,'a')
    #series of if statements with sub functions to process each category
    with open(filename, "r") as f:
        #this is definitely not the most efficient way to do this..
        #get rid of extra brackets
        #!!!IMPORTANT!!! have to work out the order of .json and .tex files so that .json gets written in the correct order
        
        '''
        figure out the order for everything: obituary,service, (DOB, DVD, Collected_Works, DOD), Member,
        (symposium, homepage, id, display_name), Degree, (Memoir), honor?, (complete_name, selected_works, oral_history),
        in_memoriam, public_record_txt, link_ls), Position, (record_txt),  Honor?, (Deceased, Fetschifts??,
        Image, alt_id, death_notice), education, (Endowment, archive, biography)) 
        '''
        #what if each if statement (and sub-function) created its own named variable and then we assemble those at the end
        #but, I don't think f.write can take variables, only strings :/
        
        for line in f:
            
            if line.startswith("\subsection*{Professional Service}"):
                n.write("\t\"Service\": [\n")
                line = f.next()
                while line.startswith("\Service"):
                    #easier way to do this: read until first } bracket, then read until next one, etc.
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #text.replace("}{",",") --> this isn't working??
                    #send year, text, etc. to separate function that will format it in json
                    format_service_json(year, text, n)
                    line = f.next()
                n.write("\t],\n")
                
                n.write("DOB, DVD, Collected Works, DOD\n")

            elif line.startswith("\subsection*{Membership}"):
                n.write("Member\n")
                line = f.next()
                while line.startswith("\Member"):
                    text = line[line.find("{")+1:line.find("}")]
                    format_member_json(text, n)
                    if f.next():
                        line = f.next() #it reaches the end of the file, so else stop iterations
                n.write("Symposium, Homepage, id, display_name\n")
                
                #degrees???? not in .tex file (oh, that i generated, joe i think is doing this)
                
            elif line.startswith("\subsection*{Education}"):
                n.write("\t\"Education\": [\n")
                line = f.next()
                while line.startswith("\Education"):
                    #easier way to do this: read until first } bracket, then read until next one, etc.
                    print "something"
                    #difference btwn Degree and Education??
                    #these categories are different in .tex and .json..?
                    line = f.next()
                n.write("\t],\n")
                
                n.write("Memoir, Honor, complete_name, Selected_Works, Oral_History, In_Memoriam, public_record.txt, Art_Exhibition\n")
                
            elif line.startswith("\subsection*{Career}"):
                n.write("\t\"Postition\": [\n")
                line = f.next()
                while line.startswith("\Position"):
                    #easier way to do this: read until first } bracket, then read until next one, etc.
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #text = position (optional), organization
                    format_career_json(year, text, n)
                    line = f.next()
                n.write("\t],\n")
                
                n.write("record_txt\n")
                
            elif line.startswith("\subsection*{Honors}"):
                #write "Sevice": [ header to file
                n.write("\t\"Honor\": [")
                line = f.next() #necessary??
                while line.startswith("\Honor"):
                    list = line.split("}")
                    if line.startswith("\Honorary"):
                        honor_type = 0
                        text = str(list[1]).strip() + " (Honorary)\t" + str(list[2]).strip()
                    else:
                        honor_type = 1
                        text = str(list[1]).strip()
                    year = line[line.find("{")+1:line.find("}")]
                    format_honors_json(year, text, n)
                    line = f.next()
                n.write("\t],")
                
                n.write("Deceased, Festschrift, Image, alt-id, Death_Notice\n")
                n.write("EDUCATION!\n")
                n.write("Endowment, Archive, Biography")
    f.close()
    n.close()
    print newfile + " written"
    return n

def format_career_json(year, text, n):
    #can combine some/all of these lines??
    n.write("\t\t{\n")
    n.write("\t\t\t\"category\": :\"position\",\n")
    n.write("\t\t\t\"text\":" + " \"" + text + "\"" + ",\n")
    n.write("\t\t\t\"year\":" + " \"" + year + "\"" + ",\n\t\t},\n")
    #don't need a comma on the last one.. fix that
    #include link_ls??

def format_honors_json(year,text, n):
    n.write("\t\t{\n")
    n.write("\t\t\t\"category\": :\"honor\",\n")
    n.write("\t\t\t\"text\":" + " \"" + text + "\"" + ",\n")
    n.write("\t\t\t\"year\":" + " \"" + year + "\"" + ",\n\t\t},\n")
    
def format_service_json(year, text, n):
    n.write("\t\t{\n")
    n.write("\t\t\t\"category\": :\"service\",\n")
    n.write("\t\t\t\"text\":" + " \"" + text + "\"" + ",\n")
    n.write("\t\t\t\"year\":" + " \"" + year + "\"" + ",\n\t\t},\n")
    
def format_member_json(text, n):
    n.write("\t\t{\n")
    n.write("\t\t\t\"category\": :\"member\",\n")
    n.write("\t\t\t\"text\":" + " \"" + text + "\"" + ",\n")



def make_ref_for_record(r): 
    title = r.get('title','').strip()
    if title == 'Untitled': title = ''
    author = r.get('author','').strip()
    if author == 'Anonymous': author = ''
    howpub  = r.get('howpublished','')
    year = r.get('year','')
    if year == 'year?': year = 'Undated'
    ref = ''
    if title:  
        if not title[-1] in '?.!': title += '.'
        ref += '<t>' + title + '</t> '
    if author: ref += '<au>' + author + '</au>. '
    ref += howpub
    #
    # Need to deal with enhancements for books somehow
    # but commenting this out for now until book processing
    # is complete.
    #
    """
    book_link_ls = []
    books = global_vars['books']
    for bkey in books.keys():
        if ref.find(bkey) >= 0:
            ref = ref.replace(bkey,books[bkey]['ref'])
            book_link_ls = books[bkey].get('link_ls',[])
    """
    #
    # for t in tag_map.keys():
    #    ref = ref.replace(t,tag_map[t])
    # ref += ' '
    # for link in r.get('link_ls',[]) + book_link_ls:
    #        link = enhance_link(link)
    #        ref += link2html(link)
    return ref

"""
read_latex will build up a large dictionary "d" with similar structure to the
dictionary returned by  read_ims_legacy  from the original code
"""

def read_latex(name):
    d = {}
    filename = name + ".tex"
    #open .tex file        
    #\\(DOB\|DOD\|Profile\|Education\|Degree\|Position\|Honor\|HonoraryDegree\|Service\|Member\|Biography)
    with open(filename, "r") as f:
        #JOE to add: bibdata part
        filestring = f.read()
        bibpart = re.split(r"\\end{filecontents}",re.split(r"\\begin{filecontents}{\\jobname.bib}", filestring)[1])[0]
        allbib=bibtex.read_bibstring(bibpart)
        # Refactor the individual bibliographic elements
        for bib in allbib:
            bib[u'id'] = bib.pop('citekey')
            bib[u'howpublished'] = display_function.howpublished_tagged(allbib[1])
            bib[u'top_line'] = bib['bibtype'] + " " + bib['id']
            bib[u'ref'] = make_ref_for_record(bib)
        # note that the individual elements of allbib still need to be added in the
        # correct section for Memoir, Biography etc., which should
        #end of bib part
        for line in f:
            if line.startswith("\subsection*{Professional Service}"):
                line = f.next()
                latex_accents.replace_latex_accents(line)
                while line.startswith("\Service"):
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #dictionaries w/in dictionaries?
                    p = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}')
                    match = p.match(line)
                    if match:
                        print match.group(1)
                    d['category'] = "service"
                    d['year'] = year
                    #d['position'] = match.group(1)
                    #d['organization'] = match.group(2)
                    if not line:
                        break
                    else:
                        line = f.next()
                    latex_accents.replace_latex_accents(line)
                    
            elif line.startswith("\subsection*{Membership}"):
                line = f.next()
                latex_accents.replace_latex_accents(line)
                while line.startswith("\Member"):
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #dictionaries w/in dictionaries?
                    match = re.match(r'{([^}]*)}{([^}]*)}{([^}]*)}', text)  # then do stuff with match.group(1) etc
                    if match:
                        print match.group(1)
                    d['category'] = "service"
                    d['year'] = year
                    #d['position'] = match.group(0)
                    #d['organization'] = match.group(1)
                    if not line:
                        break
                    else:
                        line = f.next()
                    latex_accents.replace_latex_accents(line)
    f.close()
    print name + " read"
    print d
    return d

