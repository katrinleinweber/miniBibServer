import os
import sys
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

from pprint import pprint

## Set up a global variable containing a list of the available books for cross-referencing
with open("imsBooks.bib", "r") as b:
        # bibdata part [optional]
        filestring = b.read()
        allbooks=bibtex.read_bibstring(filestring)
        imsbooks=[]
        for bib in allbooks:
            bib[u'id'] = bib.pop('citekey')
            bib[u'howpublished'] = display_function.howpublished_tagged(allbooks[0])
            bib[u'top_line'] = bib['bibtype'] + " " + bib['id']
            bib[u'ref'] = bibtex.make_ref_for_record(bib)
            # replace accents and remove brackets
            imsbooks.append({k:re.sub("[{}]", '',latex_accents.replace_latex_accents(v)) for k, v in bib.items()})

"""
  the read_latex function reads in a single .tex file and outputs
  a dictionary of person-specific elements (honors, education, etc.)

  the dictionary is will then be processed in ims_legacy.py by the make_all()
  function to create a html page.

  As a side-effect, a JSON version is written out first.
"""

'''
figure out the order for everything:
  obituary,service, (DOB, DVD, Collected_Works, DOD), Member,
  (symposium, homepage, id, display_name), Degree, (Memoir),
  honor?, (complete_name, selected_works, oral_history),
  in_memoriam, public_record_txt, link_ls, Position,
  (record_txt),  Honor?, (Deceased, Fetschifts??,
  Image, alt_id, death_notice), education, (Endowment, archive, biography)
'''

def read_latex(filename):
    data = {} #four elements (records, links_ls, books, ??) w/key 'records'
    records = []
    person = {} #should have ~ 30 total categories for each person
    service_list = []
    membership_list = []
    honors_list = []
    career_list = []
    educ_list = []
    degree_list = []
    link_list = []

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

    #reg exps to capture all lines containing cv data dependant on the number of bracketed data elements
    # NOTE: the logic only works if we escape LaTeX accents *before* applying the regular expressions
    # i.e. {abcd\'{e}} must be written {abcd&eacute} so that we can apply the regexp r'{([^}]*)}'
    p1 = re.compile(r'{([^}]*)}')
    p2 = re.compile(r'{([^}]*)}{([^}]*)}')
    p3 = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}')
    p4 = re.compile(r'{([^}]*)}{([^}]*)}{([^}]*)}{([^}]*)}')
    # For lists like {abc}{def}[ghi]
    q3 = re.compile(r'{([^}]*)}{([^}]*)}\[(.*)\]$')
    # For lists like {abc}{def}<ghi>
    r3 = re.compile(r'{([^}]*)}{([^}]*)}<([^>]*)>$')
    # For lists like {abc}{def}[ghi]<klm>
    q4 = re.compile(r'{([^}]*)}{([^}]*)}\[(.*)\]<([^>]*)>')
    # For lists like {abc}{def}<klm>[ghi]
    r4 = re.compile(r'{([^}]*)}{([^}]*)}<([^>]*)>\[(.*)\]$')

    #run reg exp to capture the listed lines
    R = re.compile(r'\\(Name|ID|AltID|AltName|DOB|DOD|BirthPlace|Profile|Homepage|Education|Degree|Position|Honor|HonoraryDegree|Service|Member|Biography|Archive|InMemoriam|Memoir|Obituary|OralHistory|ArtExhibition|Autobiography|DVD|DeathNotice|CollectedWorks|SelectedWorks|Symposium|Endowment|Festschrift){')

    with open(filename, "r") as f:
        # bibdata part [optional]
        filestring = f.read()
        if (re.search(r"\\begin{filecontents}{\\jobname.bib}", filestring) and re.search(r"\\end{filecontents}", filestring)):
            bibpart = re.split(r"\\end{filecontents}",re.split(r"\\begin{filecontents}{\\jobname.bib}", filestring)[1])[0]
            allbib=bibtex.read_bibstring(bibpart)
            # Refactor some of the individual bibliographic elements where needed
            memberbib=[]
            for bib in allbib:
                bib[u'id'] = bib.pop('citekey')
                bib[u'howpublished'] = display_function.howpublished_tagged(bib)
                bib[u'top_line'] = bib['bibtype'] + " " + bib['id']
                bib[u'ref'] = make_ref_for_record(bib)
                # fix accents and removebrackets
                memberbib.append({k:re.sub("[{}]", '',latex_accents.replace_latex_accents(v)) for k, v in bib.items()})

        for line in filestring.split('\n'):
            match = re.search(R,line)
            if match:

                # to debug: print line
                g = match.group(1)

                #Service section
                if g =="Service":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    rest = line.split("}",1)
                    text = str(rest[1]).strip()
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
                    rest = line.split("}",1)
                    text = line[line.find("{")+1:line.find("}")]
                    #match1 = p1.match(str(rest))
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
                    rest = line.split("}",1)
                    text = str(rest[1]).strip()
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
                    rest = line.split("}",1)
                    text = str(rest[1]).strip()
                    # print text
                    match = p1.match(text)
                    matchtwo = p2.match(text)
                    d['category'] = "honor"
                    d['link_ls'] = ""
                    d['year'] = year
                    if matchtwo:
                        d['text'] = matchtwo.group(1)
                        d['citation'] = matchtwo.group(2)
                    elif match:
                        d['text'] = match.group(1)
                    honors_list.append(d)

                if g == "Position":
                    d = {}
                    line = latex_accents.replace_latex_accents(line)
                    year = line[line.find("{")+1:line.find("}")]
                    rest = line.split("}",1)
                    text = str(rest[1]).strip()
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
                    rest = line.split("}",1)
                    text = str(rest[1]).strip()
                    match = p1.match(text)
                    d['category'] = "education"
                    d['year'] = year
                    if match:
                        d['text'] = match.group(1)
                    educ_list.append(d)

                if g == "Degree":
                    d = {}
                    d['category'] = "degree"
                    year = line[line.find("{")+1:line.find("}")]
                    d['year'] = year
                    line = latex_accents.replace_latex_accents(line)
                    rest = line.split("}",1)[1]
                    text = rest.strip()
                    # example: \Degree{1934}{Ph.D.}{Helsingin Yliopisto}
                    if text.endswith('}'):
                        match = p2.match(text)
                        d['type'] = match.group(1)
                        d['school'] = match.group(2)
                    # example: \Degree{1934}{Ph.D.}{Helsingin Yliopisto}[\"{U}ber eine Klasse von Riemannschen Fl\~{a}chen und ihre Uniformisierung]
                    elif text.endswith(']') and (text.count("}<") == 0) and (text.count("]<") == 0):
                        # print "Q3"
                        match = q3.match(text)
                        d['type'] = match.group(1)
                        d['school'] = latex_accents.replace_latex_accents(match.group(2))
                        d['thesis_title'] = latex_accents.replace_latex_accents(match.group(3))
                    # example: \Degree{1934}{Ph.D.}{Helsingin Yliopisto}<http://genealogy.math.ndsu.nodak.edu/id.php?id=20422>
                    elif text.endswith('>') and (text.count(">[") == 0) and (text.count("}[") == 0):
                        # print "R3"
                        match = r3.match(text)
                        d['type'] = match.group(1)
                        d['school'] = latex_accents.replace_latex_accents(match.group(2))
                        d['link_ls'] = [{"href":match.group(3)}]
                    # example: \Degree{1934}{Ph.D.}{Helsingin Yliopisto}[\"{U}ber eine Klasse von Riemannschen Fl\~{a}chen und ihre Uniformisierung]<http://genealogy.math.ndsu.nodak.edu/id.php?id=20422>
                    elif text.endswith('>') and (text.count("]<http") == 1):
                        # print "Q4"
                        match = q4.match(text)
                        d['type'] = match.group(1)
                        d['school'] = latex_accents.replace_latex_accents(match.group(2))
                        d['thesis_title'] = latex_accents.replace_latex_accents(match.group(3))
                        d['link_ls'] = [{"href":match.group(4)}]
                    # example: \Degree{1934}{Ph.D.}{Helsingin Yliopisto}<http://genealogy.math.ndsu.nodak.edu/id.php?id=20422>[\"{U}ber eine Klasse von Riemannschen Fl\~{a}chen und ihre Uniformisierung]
                    else:
                        # print "R4"
                        match = r4.match(text)
                        d['type'] = match.group(1)
                        d['school'] = latex_accents.replace_latex_accents(match.group(2))
                        d['thesis_title'] = latex_accents.replace_latex_accents(match.group(3))
                        d['link_ls'] = [{"href":match.group(4)}]
                    educ_list.append(d)

                if g == "Profile":
                    d = {}
                    text = line[line.find("{"):line.rfind("}")+1]
                    #print text
                    match = p2.match(text)
                    d['href'] = match.group(1)
                    d['anchor'] = match.group(2)
                    link_list.append(d)

                if g == "Homepage":
                    d = {}
                    d['category'] = 'homepage'
                    d['rel'] = 'homepage'
                    d['href'] = line[line.find("{")+1:line.rfind("}")]
                    
                    link_list.append(d)

                if g == "Biography":
                    biography_list.append(populate_bib_d(line,memberbib))
                if g == "Archive":
                    archive_list.append(populate_bib_d(line,memberbib))
                if g == "InMemoriam":
                    inmemoriam_list.append(populate_bib_d(line,memberbib))
                if g == "Memoir":
                    memoir_list.append(populate_bib_d(line,memberbib))
                if g == "Obituary":
                    obituary_list.append(populate_bib_d(line,memberbib))
                if g == "OralHistory":
                    oralhistory_list.append(populate_bib_d(line,memberbib))
                if g == "ArtExhibition":
                    artexhibition_list.append(populate_bib_d(line,memberbib))
                if g == "Autobiography":
                    autobiography_list.append(populate_bib_d(line,memberbib))
                if g == "DVD":
                    dvd_list.append(populate_bib_d(line,memberbib))
                if g == "DeathNotice":
                    deathnotice_list.append(populate_bib_d(line,memberbib))
                if g == "CollectedWorks":
                    collectedworks_list.append(populate_bib_d(line,memberbib))
                if g == "SelectedWorks":
                    selectedworks_list.append(populate_bib_d(line,memberbib))
                if g == "Symposium":
                    symposium_list.append(populate_bib_d(line,memberbib))
                if g == "Endowment":
                    endowment_list.append(populate_bib_d(line,memberbib))
                if g == "Festschrift":
                    festschrift_list.append(populate_bib_d(line,memberbib))

                if g == "DOB":
                    #this could probably be done w/a regexp? ... :?
                    person['DOB'] = line[line.find("{")+1:line.rfind("}")]

                if g == "DOD":
                    person['DOD'] = line[line.find("{")+1:line.rfind("}")]

                if g == "Name":
                    person['complete_name'] = latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])

                if g == "BirthPlace":
                    #print "birthplace: " + latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])
                    person['birth_place'] = latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])

                if g == "AltName":
                    person['alt_name'] = latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])

                if g == "ID":
                    person['ims_id'] = latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])

                if g == "AltID":
                    person['alt_ims_id'] = latex_accents.replace_latex_accents(line[line.find("{")+1:line.rfind("}")])

            # End of loop, now add things to the person data structure as needed

        person['Service'] = service_list
        person['Member'] = membership_list
        person['Honor'] = honors_list
        person['Position'] = career_list
        person['Education'] = educ_list
        person['Degree'] = degree_list

        person['link_ls'] = link_list

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

        # Everyone should have a name, but just in case...
        if not ('complete_name' in person):
            person['complete_name'] = "Added, Name is to be"

        person['public_record_txt'] = "" #this comes from bibtex (?)
        # print person

    f.close()
    records.append(person) #will eventually add people
    data['records'] = records

    # This would somehow be the list of 'official' links that are referenced,
    # but actually the relevant links are listed in the person's bio.
    # since I'm not sure how it is actually meant to be used, I'm deleting it
    # data['link_ls'] = []

    # This should be the list of books that are referenced in the
    # bibliography records.  We use a helper function (below) to
    # cross-reference the two lists.

    data['books'] = []

    # The memberbib variable might not be set, so put this into a "try" block
    try:
        for book in map(match_member_bibitems_into_imsbooks,memberbib):
            if book:
                data['books'].append(book)
    except: pass

    # Let's live up to the name "text_json" and dump out the text in JSON format here
    base = unicode((filename.rsplit("/",1)[1]).split('.tex',1)[0],'utf-8')
    print "making new json file: " + base + ".json"
    j = open("./jsonfiles/" + base + '.json', 'w')
    j.write(json.dumps(data,indent=4))
    j.close()

    return data

# helper
def match_member_bibitems_into_imsbooks(item):
    if item.has_key('crossref'):
        return filter(lambda book: book['id'] == item['crossref'], imsbooks)[0]

def make_ref_for_record(r):
    #pprint (r)
    author = ''
    editor = ''
    crossref=''
    title = r.get('title','').strip()
    if title == 'Untitled': title = ''
    if r.has_key('author'):
        author = r.get('author','').strip()
        if author == 'Anonymous':
            author = ''
    if r.has_key('editor'):
        editor = r.get('editor','').strip()
        if editor == 'Anonymous':
            editor = ''
    if r.has_key('crossref'):
        crossref = r.get('crossref','').strip()
    howpub  = r.get('howpublished','')
    year = r.get('year','')
    if year == 'year?': year = 'Undated'
    ref = ''
    if title:
        if not title[-1] in '?.!': title += '.'
        ref += '<t>' + title + '</t> '
    if author: ref += '<au>' + author + '</au>. '
    if editor: ref += '<ed>' + editor + '</ed>. '
    if crossref: ref += '<inc>' + crossref + '</inc>. '
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

def populate_bib_d (line,thebib):
    d = {}
    id = line[line.find("{")+1:line.rfind("}")]
    for bib in thebib:
        if (bib['id'] == id):
            if bib.has_key('author'):
                d['author'] = latex_accents.replace_latex_accents(bib['author'])
            if bib.has_key('editor'):
                d['editor'] = latex_accents.replace_latex_accents(bib['editor'])
            if bib.has_key('crossref'):
                d['editor'] = bib['crossref']
            d['title'] = re.sub("{|}","",latex_accents.replace_latex_accents(bib['title']))
            d['bibtype'] = bib['bibtype']
            d['topline'] = bib['bibtype'] + " " + bib['id']
            d['year'] = bib['year']
            d['howpublished'] = bib['howpublished']
            d['ref'] = bib['ref']
            d['id'] = bib['id']
            return d
