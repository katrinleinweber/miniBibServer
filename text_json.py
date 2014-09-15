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

'''
figure out the order for everything: obituary,service, (DOB, DVD, Collected_Works, DOD), Member,
(symposium, homepage, id, display_name), Degree, (Memoir), honor?, (complete_name, selected_works, oral_history),
in_memoriam, public_record_txt, link_ls), Position, (record_txt),  Honor?, (Deceased, Fetschifts??,
Image, alt_id, death_notice), education, (Endowment, archive, biography))
'''

#this function reads in a single .tex file and outputs a dictionary of person-specific elements (honors, education, etc.)
#the dictionary is then processed in ims_legacy.py byt the make_all() function to create a html page
def read_latex(name):
    #data{} includes
    data = {} #four elements (records, links_ls, books, ??) w/key 'records'
    records = []
    person = {} #should have ~ 30 total categories for each person
    service_list = []
    membership_list = []
    honors_list = []
    career_list = []
    educ_list = []
    degree_list = []

    biography_list = []
    archive_list = []
    inmemoriam_list = []
    memoir_list = []
    obituary_list = []
    oralhistory_list = []
    artexhibition_list = []
    autobiography_list = []
    dvd_list = []
    deathnotice_list = []
    collectedworks_list = []
    selectedworks_list = []
    symposium_list = []
    endowment_list = []
    festschrift_list = []

    filename = name

    #reg exps to capture all lines containing cv data dependant on the number of bracketed data elements
    p1 = re.compile(r'{([^}]*)}')
    p2 = re.compile(r'{([^}]*)}{([^}]*)}')
    p3 = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}')
    p4 = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}{([^}]*)}')

    #run reg exp to capture the listed lines
    R = re.compile(r'\\(Name|DOB|DOD|Profile|Education|Degree|Position|Honor|HonoraryDegree|Service|Member|Biography|Archive|InMemoriam|Memoir|Obituary|OralHistory|ArtExhibition|Autobiography|DVD|DeathNotice|CollectedWorks|SelectedWorks|Symposium|Endowment|Festschrift){')

    with open(filename, "r") as f:
        # bibdata part [optional]
        filestring = f.read()
        if (re.search(r"\\begin{filecontents}{\\jobname.bib}", filestring) and re.search(r"\\end{filecontents}", filestring)):
            bibpart = re.split(r"\\end{filecontents}",re.split(r"\\begin{filecontents}{\\jobname.bib}", filestring)[1])[0]
            allbib=bibtex.read_bibstring(bibpart)
            # Refactor some of the individual bibliographic elements where needed
            for bib in allbib:
                bib[u'id'] = bib.pop('citekey')
                bib[u'howpublished'] = display_function.howpublished_tagged(allbib[0])
                bib[u'top_line'] = bib['bibtype'] + " " + bib['id']
                bib[u'ref'] = make_ref_for_record(bib)
                # print bib[u'ref']
        # note that the individual elements of allbib still need to be added in the
        # correct section for Memoir, Biography etc. - they can be cross-referenced
        # from the later section, which requires changing
        # end of bibdata part
        # loop over lines

        for line in filestring.split('\n'):
            match = re.search(R,line)
            if match:
                # print line
                g = match.group(1)
                #Service section
                if g =="Service":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
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
                    service_list.append(d)

                # per request we aren't populating the membership section
                '''
                if g == "Member":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    list = line.split("}",1)
                    text = line[line.find("{")+1:line.find("}")]
                    #match1 = p1.match(str(list))
                    #print match1.group(1)
                    d['category'] = "member"
                    d['link_ls'] = ""
                    if match:
                        d['text'] = text
                    membership_list.append(d)
                '''

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

                if g == "Honor":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
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

                if g == "Position":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    match = p2.match(text)
                    d['category'] = "position"
                    d['year'] = year
                    if match:
                        d['text'] = match.group(1) + ', ' + match.group(2)
                    career_list.append(d)

                if g == "Education":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    match = p1.match(text)
                    d['category'] = "education"
                    d['year'] = year
                    if match:
                        d['text'] = match.group(1)
                    educ_list.append(d)

                #need genealogy links?
                if g == "Degree":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    list = line.split("}",1)
                    text = str(list[1]).strip()
                    d['category'] = "degree"
                    d['year'] = year
                    #test for optional fields
                    if text.count('}') <= 3:
                        match = p2.match(text)
                        d['type'] = match.group(1)
                        d['school'] = match.group(2)
                    else:
                        match = p4.match(text)
                        d['type'] = match.group(1)
                        d['school'] = match.group(2)
                        d['thesis_title'] = match.group(3)
                        #has to be a LIST of links. work on this
                        #d['link_ls'].append(match.group(4))
                    educ_list.append(d)

                if g == "Biography":
                    biography_list.append(populate_bib_d(line,allbib))
                if g == "Archive":
                    archive_list.append(populate_bib_d(line,allbib))
                if g == "InMemoriam":
                    inmemoriam_list.append(populate_bib_d(line,allbib))
                if g == "Memoir":
                    memoir_list.append(populate_bib_d(line,allbib))
                if g == "Obituary":
                    obituary_list.append(populate_bib_d(line,allbib))
                if g == "OralHistory":
                    oralhistory_list.append(populate_bib_d(line,allbib))
                if g == "ArtExhibition":
                    artexhibition_list.append(populate_bib_d(line,allbib))
                if g == "Autobiography":
                    autobiography_list.append(populate_bib_d(line,allbib))
                if g == "DVD":
                    dvd_list.append(populate_bib_d(line,allbib))
                if g == "DeathNotice":
                    deathnotice_list.append(populate_bib_d(line,allbib))
                if g == "CollectedWorks":
                    collectedworks_list.append(populate_bib_d(line,allbib))
                if g == "SelectedWorks":
                    selectedworks_list.append(populate_bib_d(line,allbib))
                if g == "Symposium":
                    symposium_list.append(populate_bib_d(line,allbib))
                if g == "Endowment":
                    endowment_list.append(populate_bib_d(line,allbib))
                if g == "Festschrift":
                    festschrift_list.append(populate_bib_d(line,allbib))

                if g == "DOB":
                    #this could probably be done w/a regexp? ... :?
                    #R = re.compile(r'.\{$\{')
                    #   ???? tomorrow I shall learn
                    person['DOB'] = line[line.find("{")+1:line.find("}")]

                if g == "DOD":
                    person['DOD'] = line[line.find("{")+1:line.find("}")]

                if g == "Name":
                    person['complete_name'] = line[line.find("{")+1:line.find("}")]

            # End of loop, add things to the person data structure as needed

        person['Service'] = service_list
        person['Member'] = membership_list
        person['Honor'] = honors_list
        person['Position'] = career_list
        person['Education'] = educ_list
        person['Degree'] = degree_list

        person['Biography']        = biography_list
        person['Archive']          = archive_list
        person['Memoir']           = memoir_list
        person['Art_Exhibition']   = artexhibition_list
        person['Collected_Works']  = collectedworks_list
        person['DVD']              = dvd_list
        person['Endowment']        = endowment_list
        person['Festschrift']      = festschrift_list
        person['Autobiography']    = autobiography_list
        person['Oral_History']     = oralhistory_list
        person['Selected_Works']   = selectedworks_list
        person['Symposium']        = symposium_list
        person['Death_Notice']     = deathnotice_list
        person['In_Memoriam']      = inmemoriam_list
        person['Obituary']         = obituary_list

        # NB. we need to update ims_legacy_latex to get these from colon-formatted
        # data!
        if not ('complete_name' in person):
            person['complete_name'] = "Added, Name is to be"

        person['public_record_txt'] = "" #this comes from bibtex (?)
        # print person

    f.close()
    records.append(person) #will eventually add people
    data['records'] = records
    data['link_ls'] = [{'category_ls': [u'committee'], 'href': u'http://academic-senate.berkeley.edu/committees/frl', 'anchor': u'Faculty Research Lecture Committee, University of California, Berkeley'}, {'category_ls': [u'lecture'], 'href': u'http://www.urel.berkeley.edu/faculty/history.html', 'anchor': u'Faculty Research Lecturer, University of California, Berkeley'}]
    data['books'] = []
    print filename + " read"
    #print data
    return data

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

    return ref

def populate_bib_d (line,allbib):
    d = {}
    id = line[line.find("{")+1:line.find("}")]
    for bib in allbib:
        if (bib['id'] == id):
            d['author'] = latex_accents.replace_latex_accents(bib['author'])
            d['title'] = re.sub("{|}","",latex_accents.replace_latex_accents(bib['title']))
            d['bibtype'] = bib['bibtype']
            d['topline'] = bib['bibtype'] + " " + bib['id']
            d['year'] = bib['year']
            d['howpublished'] = bib['howpublished']
            d['ref'] = bib['ref']
            d['id'] = bib['id']
            return d
