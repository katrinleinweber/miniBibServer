import os
import json 
import glob
import time
import datetime
time_stamp = unicode( datetime.datetime.now().isoformat().split('.')[0], 'utf-8')   
import random
import latex_accents
import re

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
    
def read_latex(name):
    data = {} #four elements (records, links_ls, books, ??) w/key 'records'
    records = [] 
    person = {} #should have ~ 30 total categories for each person
    service_list = []
    membership_list = []
    honors_list = []
    
    filename = name + ".tex"
    p3 = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}')
    p2 = re.compile(r'{([^}]*)}{([^}]*)}')
    p1 = re.compile(r'{([^}]*)}')
    
    #JOE to add: bibdata part
    
    #end of bib part
    
    R = re.compile(r'\\(DOB|DOD|Profile|Education|Degree|Position|Honor|HonoraryDegree|Service|Member|Biography){')
    with open(filename, "r") as f:
        for line in f:
            #if line.startswith("\subsection*{Professional Service}"):
            match = re.search(R,line)
            if match:
                g = match.group(1)
                #print g
                if g =="Service":
                    #print line
                    d = {}
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #dictionaries w/in dictionaries?
                    match = p2.match(text)
                    d['category'] = "service"
                    d['year'] = year
                    d['link_ls'] = ""
                    d['text'] = ""
                    if match:
                        d['text'] = match.group(1) + ", " + match.group(2)
                    latex_accents.replace_latex_accents(line)
                    service_list.append(d)
                person['Service'] = service_list
                
                if g == "Member":
                    d = {}
                    list = line.split("}",1)
                    text = line[line.find("{")+1:line.find("}")]
                    #match1 = p1.match(str(list))
                    #print match1.group(1)
                    d['category'] = "member"
                    d['link_ls'] = ""
                    if match:
                        d['text'] = text
                    latex_accents.replace_latex_accents(line)
                    membership_list.append(d)
                person['Member'] = membership_list
                
                if g == "HonoraryDegree":
                    d = {}
                    latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    match = p2.match(text)
                    d['category'] = "honor"
                    d['link_ls'] = ""
                    if match:
                        d['year'] = year
                        d['text'] = match.group(1) + ' (Honorary)\t' + match.group(2)
                    honors_list.append(d)
                person['Honor'] = honors_list
                        
                if g == "Honor":
                    d = {}
                    latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    match = p1.match(text)
                    d['category'] = "honor"
                    d['link_ls'] = ""
                    d['text'] = text
                    if match:
                        d['year'] = year
                        d['text'] = match.group(1)
                    honors_list.append(d)
                person['Honor'] = honors_list
               
                
            #update ims_legacy_latex to get these from colon-formatted data
        person['complete_name'] = name  #DEPENDS ON FILE TO BE READ!!
        person['Education'] = []
        person['Degree'] = []
        person['Obituary'] = []
        person['DOB'] = []
        person['Position'] = []
        person['public_record_txt'] = "" #this comes from bibtex
            
            
            #Bibtex section (check over w/ joe)
            #elif line.startswith("\Member")
            
            
    f.close()
    records.append(person) #will eventually add people
    data['records'] = records
    data['link_ls'] = [{'category_ls': [u'committee'], 'href': u'http://academic-senate.berkeley.edu/committees/frl', 'anchor': u'Faculty Research Lecture Committee, University of California, Berkeley'}, {'category_ls': [u'lecture'], 'href': u'http://www.urel.berkeley.edu/faculty/history.html', 'anchor': u'Faculty Research Lecturer, University of California, Berkeley'}]
    data['books'] = []
    print filename + " read"
    #print data
    return data

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

