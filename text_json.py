import json 
import glob
import time
import datetime
time_stamp = unicode( datetime.datetime.now().isoformat().split('.')[0], 'utf-8')   
import random

def make_all():
    #runs publish_json on all .tex files in a directory
    print "done!"

def publish_json(name):
    filename = name + ".tex"
    newfile = name + ".json"
    content = {}
    #open .tex file
    f = open(filename)
    n = open(newfile,'w')
    #series of if statements with sub functions to process each category
    with open(filename, "r") as f:
        #this is definitely not the most efficient way to do this..
        #get rid of extra brackets
        
        '''
        figure out the order for everything: obituary,service, (DOB, DVD, Collected_Works, DOD), Member,
        (symposium, homepage, id, display_name), Degree, (Memoir), honor?, (complete_name, selected_works, oral_history),
        in_memoriam, public_record_txt, link_ls), Position, (record_txt),  Honor?, (Deceased, Fetschifts??,
        Image, alt_id, death_notice), education, (Endowment, archive, biography)) 
        '''
        
        for line in f:
            if line.startswith("\subsection*{Career}"):
                n.write("\t\"Postition\": [\n")
                line = f.next()
                while line.startswith("\Position"):
                    #easier way to do this: read until first } bracket, then read until next one, etc.
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    #send year, text, etc. to separate function that will format it in json
                    format_career_json(year, text, n)
                    line = f.next()
                n.write("\t],\n")
                
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
                    print list
                    format_honors_json(year, text, n)
                    line = f.next()
                n.write("\t],")
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
