# coding=utf-8
import re
import json 
import glob
import time
import datetime
time_stamp = unicode( datetime.datetime.now().isoformat().split('.')[0], 'utf-8')   
import random
import latex_accents
import pprint

pp = pprint.PrettyPrinter(indent=4)

## set some global variables for convenience of use
global_vars = {}
global_vars['published_files_directory'] = './published_files/'

global_vars['latex_beg'] = '\\documentclass[letterpaper]{article}\n\\usepackage{imscv}\n\\addbibresource{imsBooks.bib}\n\\addbibresource{\\jobname.bib}\n\\usepackage{filecontents}\n\\begin{filecontents}{\\jobname.bib}\n'
global_vars['latex_med'] = '\n\\end{filecontents}\n\n\\begin{document}'
global_vars['latex_end'] = '\\end{document}'

### tool for breaking long lines nicely
txt = '''   :citation For developing new statistical methods for diffusion and other stochastic processes, for identifying and opening new fields of applications of statistics including nonparametric inference and testing to the analysis and pricing of financial instruments, and for his conscientious professional service'''
def break_lines(txt,nchars):
    words = txt.split()
    broken_lines = []
    thisline = ''
    while 1:
        thisline += words[0] + ' '
        if len(thisline) > nchars:
            thisline = ' '.join(thisline.split()[0:-1])
            broken_lines += [ thisline ]
            thisline = words[0] + ' '
        else:
            pass
        words = words[1:]
        if not words: 
            broken_lines += [ thisline ]
            break
    return broken_lines

def indent(txt):
    words = txt.split()
    if len(words) > 0:
        word = words[0]
        pre,post = txt.split(word,1)
        return pre
    else:
        return ''

def normalize_indent(txt):
    if not indent(txt): return txt
    else: 
        words = txt.split()
        return '\t' + ' '.join(txt.split())

def break_line_txt(txt,nchars):
    lines = break_lines(txt,nchars)
    if len(lines) == 0: return ''
    else:
        lines = [ indent(txt) + lines[0]] +  [ '\t' + line for line in lines[1:]]
        lines = [ normalize_indent(line) for line in lines]
        return '\n'.join(lines)

def break_txt(txt, nchars):
    p = ''
    for line in txt.split('\n'):
        if len(line)  > nchars:
            if line.strip()[0] == ':': 
                p += '\n' + break_line_txt(line,nchars)
            else: p += '\n' + normalize_indent(line)
        else: p += '\n' + normalize_indent(line)
    p += '\n'
    return p


### tools for handling years 
digits = '0123456789'

def get_year2(line,digs):
    y12 = ''
    y34 = ''
    rest = ''
    yinsts = line.split(digs)
    if len(yinsts) > 0:
        for yinst in yinsts[1:]:
            try:
                y34 = yinst.split()[0]
                for x in (',.<)'): y34 = y34.split(x)[0]
                if len(y34) == 2 and y34[0] in digits and y34[1] in digits:
                    return digs + y34
                else: pass
            except: pass
    return ''

def get_years2(line,digs):
    """ returns a list of 4 digit strings that are credibly years beginning with 2 digits digs """
    y12 = ''
    y34 = ''
    rest = ''
    years = []
    yinsts = line.split(digs)
    if len(yinsts) > 0:
        for yinst in yinsts[1:]:
            try:
                y34 = yinst.split()[0]
                for x in (',.<)'): y34 = y34.split(x)[0]
                if len(y34) == 2 and y34[0] in digits and y34[1] in digits:
                    years += [digs + y34]
            except: pass
    return years

def get_year_from_str(line):
    y = get_year2(line,'19')
    if not y: y = get_year2(line,'20')
    try: 
        if int(y) > 2014: y = str(2014)
    except: y = ''
    return y

def get_years_from_str(line):
    return get_years2(line,'19') + get_years2(line,'20')

def get_year_from_record(r):
        """ make best effort to extract a year string from a record, returns '' if none found """
        y = r.get('year','')
        if not y: 
            y = get_year_from_str(   r.get('howpublished','')   )
        if not y:   ## this works for arxiv records #arxiv:published": "2005-03-03T08:34:51Z"
            y = r.get('arxiv:published','').split('-')[0]
        return y             

def get_year(x):
    if type(x) in [type(u'txt'),type('txt')]:
        return  get_year_from_str(x)
    elif type(x) == type({}):
        return get_year_from_record(x)
    else: return ''

def year_examples():
    line = 'Electron. Trans. Numer. Anal. (ETNA) 36 (2009), 27-38. ps&nbsp'
    line2 = 'Electron. Trans. Numer. Anal. (ETNA) 36 (2009), 27-38. ps&nbsp 1984 1963)'
    line = '(<y>2006</y>). <rel>In </rel><inc>booktitle:encyclopedia-of-statistical-sciences</inc>'
    print get_year(line)
    #print get_years_from_str(line2)




def year_cmp(a,b): 
    try: return cmp( a.get('year','3000'),b.get('year','3000'))
    except:
        print 'year_cmp failed for '
        print a
        print b
        return 0

month_ls = 'January February    March   April   May June    July    August  September   October November    December'.split()
month = {}
for i in range(12): month[ str( i + 1) ] = month_ls[i]
for i in range(12): month[ '0' + str( i + 1) ] = month_ls[i]
    

def parse_date(dt):
    d = {}
    ss = dt.split('-')
    if len(ss) == 0:
        pass
    if len(ss) >= 1:
        d['year'] = ss[0].strip()
    if len(ss) >= 2:
        d['month'] = month[ss[1]].strip()
    if len(ss) >= 3:
        day = ss[2].strip()
        if day and day[0] == '0':
            day = day[1]
        d['day'] = day.strip()
    return d

def show_date(dt):
    d = parse_date(dt)
    if d.has_key('day'): return d['day'] + ' ' + d['month'] + ' ' + d['year']
    elif d.has_key('month'): return d['month'] + ' ' + d['year']
    elif d.has_key('year'): return d['year']
    else: return ''

def getf(d,k):
    dd = d.get(k,[])
    if len(dd) > 0: return dd[0]
    else: return ''

# Create a global variable describing categories of published works    
bio_cat_plurals = '''
    Biography       Biographies
    Symposium       Symposia
    Archive         Archives
    Art_Exhibition  Art_Exhibitions
    Collected_Works Collected_Works
    Selected_Works  Selected_Works
    DVD             DVDs
    Endowment       Endowments
    Festschrift     Festschriften
    Memoir          Memoirs
    Oral_History    Oral_History
    Death_Notice    Death_Notices
    Obituary        Obituaries
    In_Memoriam     Memorials
    '''

bio_cat_plural = {}
bio_cat_order = []
lines = bio_cat_plurals.split('\n')
for line in lines:
    try: 
        k,v = line.split()
        bio_cat_plural[k] = v
        bio_cat_order += [k]
    except: pass


# Note: this function has been adjusted from the HTML version in a very hacky way,
# it should really be cleaned up and replaced when we're ready to ship.
#
# Notes on this format:  <rel> is a reference 
def make_tag_map():
    tag_map_lines = '''
    <au>    author
    <author>    author
    <cit>    <span class="bib-citation">
    <ed>    editor
    <year>      year
    <rel>      <span class="bib-relation">
    <y>      year
    <journal>      journal
    <j>      journal
    <title>      title
    <t>      title
    <bt>      <span class="bib-title">
    <booktitle>    booktitle
    <webcollection>    booktitle
    <v>      volume
    <vol>      volume
    <volume>      volume
    <howpublished>      <span class="bib-howpublished">
    <howpub>      <span class="bib-howpublished">
    <pages>      pages
    <pp>      pages
    <series>      series
    <pub>      publisher
    <publisher>      publisher
    <address>      address
    '''
    tag_map = {}
    lines = tag_map_lines.split('\n')
    for line in lines:
        try:
            k,v = line.strip().split('>',1)
            k = k.strip()
            v = v.strip()
            tag_map[k+ '>'] = v
            tag_map['<' + short_tag[k[1:]] + '>'] = v
        except:
            pass
    for tag in tag_map.keys():
        tag_map[tag.replace('<','</')] = '}\n'
    return tag_map

tag_map = make_tag_map()



def make_link_ls():
    this_dir = './'
    link_ls = []
    infile = open(this_dir + 'organizations.txt')
    inlines = infile.readlines()
    for line in inlines:
        line = unicode(line,'utf-8')
        try:
            k,v = line.split(None,1)
            if k[0:4] == 'http':
                link = {}
                link['href'] = k
                try: v = json.loads('"' + v + '"')
                except: pass
                link['anchor'] =  ' '.join(v.split())
                link_ls += [link]
            else: pass # print line
        except: pass # print line
    return link_ls

def make_link_dict():
    d = {}
    link_ls = make_link_ls()
    for link in link_ls:
        d[ link['anchor'] ] = link['href']
    return d

link_dict = make_link_dict()

def randtag():
    return str(random.randint(100,1000000) )

def lines2link_ls(lines):
    link_ls = []
    for line in lines.split('\n'):
            line = line.strip()
            if not line[0:4] == 'http': pass ## print line
            else:
                words = line.split()
                link = {}
                link['href'] = words[0]
                anchor = ' '.join(words[1:])
                if anchor: rel = words[1]
                else: rel = ''
                if rel in 'homepage pubspage bookspage profilepage'.split():
                    link['rel'] = rel
                    link['anchor'] = ' '.join(words[2:])
                elif anchor:
                    link['anchor'] = anchor
                else: link['anchor'] = ''
                link_ls += [link]
    return link_ls


def item_cmp(x,y):
    return - cmp( len(x['anchor']), len(y['anchor']) )
    
def links_txt2ls(links_txt):
    inlines = links_txt.split('\n')
    lines = []
    dls = []
    for line in inlines:
        words = line.split()
        if words:
            d = {}
            urls = [ w for w in words if w[0:4] == 'http']
            if not len(urls) == 1:
                print 'Error with ', str(len(urls)) , 'urls in: ' ,line
                continue
            text_words = [ w for w in words if not w[0:4] == 'http']
            text_words = [ w for w in text_words if not w[0] == '[']
            text_words = [ w for w in text_words if not w[-1] == ']']
            key_words = [ w for w in words if w[0] == '[' and w[-1] == ']']
            text = ' '.join(text_words) 
            d['anchor'] = text
            d['href'] = urls[0]
            d['category_ls'] = [w[1:-1] for w in key_words]
            dls += [d]
    dls.sort(item_cmp)
    return dls

def item2link(d):
    return '<a href="' + d['href'] + '">'  + d['anchor'] + '</a>'

def item2txt(d):
    return d['anchor'] + ' ' +  ' '.join(d.get('category_ls',[])) + ' ' + d['href'] + '\n'

def add_links(txt, link_ls):
    for ii in range( len(link_ls) ):
        item = link_ls[ii]
        txt = txt.replace( item['anchor'], 'XX' + str(ii) + 'XX' )
    for ii in range( len(link_ls) ):
        item = link_ls[ii]
        txt = txt.replace('XX' + str(ii) + 'XX' , item2link(item))
    return txt

def list_links(txt, link_ls):
    out_txt = '::links\n'
    for ii in range( len(link_ls) ):
        item = link_ls[ii]
        txt = txt.replace( item['anchor'], 'XX' + str(ii) + 'XX' )
    for ii in range( len(link_ls) ):
        item = link_ls[ii]
        if txt.find('XX' + str(ii) + 'XX') >= 0:
            out_txt += item2txt(item)
    return out_txt

#links = links_txt2ls()
#for link in links:
#    print json.dumps(link,indent=4)
#print add_links(txt, links)
#print list_links(txt, links)




def read_ims_legacy(f='ims_legacy'):
    data = {}
    dls = []
    infile = open(f + '.txt')
    instring = infile.read()
    ##instring = instring.replace(':description','    :citation')   ##  to be deprecated soon
    instring = unicode(instring,'utf-8')
    meta = {}
    metatxt = instring.split('::')[1]
    meta['record_txt'] =  '::' + metatxt.strip() + '\n\n'
    meta['bibtype'],rest= metatxt.split(None,1)
    meta['id'],rest= rest.split(None,1)
    rest = '\n' + rest.strip()
    secs = rest.split('\n:')[1:]
    for sec in secs:
        k,v = sec.split(None,1)
        meta[k] = v
    data['metadata'] = meta
    for x in instring.split('::person')[1:]:
        x = x.split('\n::')[0]
        d = {}
        d['record_txt'] = '::person ' + x.strip() + '\n'
        lines = d['record_txt'].split('\n')
        lines = [line for line in lines if not line.find('Email') >= 0 ]
        pubrecord = '\n'.join(lines) + '\n'
        d['public_record_txt'] =  break_txt(pubrecord,80)
        secs = x.split('\n:')
        toplines = secs[0].strip()
        d['id'], toplines  = toplines.split(None,1)
        try: name,toplines = toplines.split('\n',1)
        except: 
            name = toplines
            toplines = ''
        d['complete_name'] = name
        #d['link_lines'] = toplines
        d['link_ls'] = lines2link_ls(toplines)
        for sec in secs[1:]:
            words = sec.split()
            key = words[0]
            if len(words) > 1:
                val = sec.split(None,1)[1]   ## keep newlines
            else: val = ''
            if d.has_key(key): d[key] += [val]
            else: d[key] = [val]
        d['Honor'] = [ read_honor(x) for x in d.get('Honor',[]) ]
        d['Degree'] = [ read_degree(x) for x in d.get('Degree',[]) ]
        d['Education'] = [ read_education(x) for x in d.get('Education',[]) ]
        d['Service'] = [ read_service(x) for x in d.get('Service',[]) ]
        d['Position'] = [ read_position(x) for x in d.get('Position',[]) ]
        d['Member'] = [ read_member(x) for x in d.get('Member',[]) ]
        d['Image'] = [ read_image(x) for x in d.get('Image',[]) ]
        d['Homepage'] = [ read_homepage(x) for x in d.get('Homepage',[]) ]
        for k in bio_cat_order:
            d[k] = [ read_bio(x) for x in d.get(k,[]) ]
        dls += [d]
    links_txt = instring.split('::links',1)[1].split('\n::')[0]
    data['link_ls'] = links_txt2ls(links_txt)
    data['records'] = dls
    books = instring.split('::book')[1:]
    book_dict = {}
    for b in books:
        b = 'book' + b
        d = read_book(b)
        del d['top_line']
        book_dict[ d['id'] ] = d
    data['books'] = book_dict
    links_txt = instring.split('::links',1)[1].split('\n::')[0]
    data['link_ls'] = links_txt2ls(links_txt)
    return data

def publish_ims_legacy(f='ims_legacy'):
    """ create public version of data by deletion of all email addresses """
    out_dir = global_vars['published_files_directory'] 
    data = {}
    dls = []
    infile = open(f + '.txt')
    instring = infile.read()
    ##instring = instring.replace(':description','    :citation')   ##  to be deprecated soon
    instring = unicode(instring,'utf-8')
    instring = instring.replace('$time_stamp$', time_stamp)
    lines = instring.split('\n')
    lines = [line for line in lines if not line.find('Email') >= 0 ]
    txt = '\n'.join(lines) + '\n'
    out_fname = out_dir + 'imslegacy_data'
    #outfile = open('/accounts/projects/jpopen/apache/htdocs/tmp/imslegacy/imslegacy_data.txt','w')
    outfile = open(out_fname + '.txt','w')
    outfile.write(txt.encode('utf-8'))
    outfile.close()
    print ' wrote to ' + out_fname + '.txt'
    ##print ' published at http://bibserver.berkeley.edu/tmp/imslegacy/imslegacy_data.txt'

    #data = read_ims_legacy('/accounts/projects/jpopen/apache/htdocs/tmp/imslegacy/imslegacy_data')
    data = read_ims_legacy(out_fname)
    #outfile = open('/accounts/projects/jpopen/apache/htdocs/tmp/imslegacy/imslegacy_data.json','w')
    outfile = open(out_fname + '.json','w')
    outfile.write(json.dumps(data,indent=4).encode('utf-8'))
    outfile.close()
    print ' wrote to ' + out_fname + '.json'
    #print ' wrote to /accounts/projects/jpopen/apache/htdocs/tmp/imslegacy/imslegacy_data.json'
    #print ' published at http://bibserver.berkeley.edu/tmp/imslegacy/imslegacy_data.json'
    
        
def write_ims_legacy(data,fname):
    meta = data['metadata']
    p = ''
    p += '::' + meta['bibtype'] + ' ' + meta['id'] + '\n'
    p += ':title ' + meta['title'] + '\n'
    for k in meta.keys():
        if not k in 'bibtype id title'.split():
            if not k[-3:] == '_ls': 
                meta[k] = [ meta[k]]
            for v in meta[k]:
                p += ':' + k + ' ' + meta[k] + '\n'
    p += '\n'
    for d in data['records']:
        p += person_record2txt(d)
    outfile = open(fname + '.txt','w')
    outfile.write(p.encode('utf-8'))
    outfile.close()


def id2url(k,v):
        if k == 'zb-author-id': h = 'http://zbmath.org/authors/?q=ai:' + v
        elif k == 'mr-author-id': h =  'http://www.ams.org/mathscinet/search/author.html?mrauthid=' + v
        elif k == 'mg-author-id': h =  'http://genealogy.math.ndsu.nodak.edu/id.php?id=' + v
        elif k == 'mas-author-id': h =  'http://academic.research.microsoft.com/Author/' + v
        else: h = k + ':' + v
        return h

def ids_dict(d):
    iii = {}
    for link in d['link_ls']:
        try: 
            iii['zb-author-id'] = link['href'].split('http://zbmath.org/authors/?q=ai:',1)[1]
            continue
        except: pass
        try: 
            iii['mr-author-id'] =  link['href'].split('http://www.ams.org/mathscinet/search/author.html?mrauthid=',1)[1]
            continue
        except: pass
        try: 
            iii['mg-author-id'] =  link['href'].split('http://genealogy.math.ndsu.nodak.edu/id.php?id=',1)[1]
            continue
        except: pass
    return iii

def make_xml_person(d):
    iii = ids_dict(d)
    d.update(iii)
    infile = open('template.xml')
    instring = infile.read()
    xml = unicode(instring,'utf-8')
    passd = {}
    passd['id'] = d['id']
    for k in 'display_name complete_name last_name DOB DOD mr-author-id zb-author-id mg-author-id'.split():
        v = d.get(k,'')
        if type(v) == type([]):
            try: passd[k] = v[0]
            except: passd[k] = ''
        else: passd[k] = v
    #for k in 'DOD DOB'.split():
    #    passd[k] = clean_date(passd[k])
    name = passd.get('display_name', '').strip()
    if not name: 
        name = passd.get('complete_name','')
    if not name:
        print 'missing name for '
        print json.dumps(d,indent=4)
    passd['last_first_name'] = name
    try: passd['first_first_name'] = first_first(name)
    except: 
        print 'Unable to make first_first for :' ,name
    passd['last_name'] = name.split(',')[0]
    #passd['html'] = d['covertext_html']
    for k in passd.keys():
        xml = xml.replace('$' + k + '$',passd[k])
    return xml

def make_xml(dls):
    out_dir = global_vars['published_files_directory'] 
    xml_wrapper = '''<?xml version="1.0" encoding="UTF-8"?>
<ims-authors-data>
<!-- Generated by BibServer System $time_stamp$ -->
$xml_data$
</ims-authors-data>
    '''
    xml = ''
    for d in dls:
        xml += make_xml_person(d)
    xml_wrapper = xml_wrapper.replace('$time_stamp$',time_stamp)
    xml_wrapper = xml_wrapper.replace('$xml_data$',xml)
    #outfile = open('/accounts/projects/jpopen//apache/htdocs/tmp/celebratio_ims_legacy.xml','w')
    #outfile = open('/accounts/projects/jpopen/apache/htdocs/tmp/imslegacy/celebratio.xml','w')
    outfname = out_dir + 'celebratio.xml'
    outfile = open(outfname, 'w')
    outfile.write(xml_wrapper.encode('utf-8'))
    outfile.close()
    print 'wrote to ' + outfname
    ###print 'wrote to http://bibserver.berkeley.edu/tmp/imslegacy/celebratio.xml'

def display_function(display_style,r):
    if display_style == 'json_display':
        h = '<td><pre>' + json.dumps(r,indent=4) + '</pre></td>'
    elif display_style == 'one_line':
        h = '<td>' + r['complete_name']  + '</td><td>'
        h += make_dates_html(r)
        h += '</td>'
    elif display_style == 'images':
        h = '<td>' + r['complete_name']  + '</td><td>'
        h += top_links_html(r)
        
        h += make_images_html(r)
    elif display_style == 'html':
        h = '<td>' 
        d = add_html(r)
        h += d['html']
        h += '</td>'
    else: 
        h = '<td> display style "' + display_style +'" not available for this source</td>'
    return h

def display_data(passd):
    meta = passd
    q = passd['q'].strip()
    try: pageNumber=int(passd['pageNumber'])
    except: pageNumber =1
    try: itemsPerPage=int(passd['itemsPerPage'])
    except: itemsPerPage=20
    data = read_ims_legacy()
    records = data['records']
    for w in q.split():
        records = [ r for r in records if str(r).find(w) >= 0]
    ## should fold as much as possible of passd into meta
    meta.update( data['metadata'] )  ## so passd gets overwritten. Hopefully no issues there
    meta['pageNumber'] = pageNumber
    totalResults = len(records)
    meta['totalResults']  = totalResults
    format_options_txt = '''         
    two_lines  Two Lines
    one_line   One Line
    images   Images
    json_display JSON Display
    html HTML
    '''
    '''
    json    JSON Export
    '''
    ## these are keys to the dictionary of display_functions returned by the display_function module
    format_ls = []
    for line in format_options_txt.split('\n'):
        if line.strip():
            k,v = line.split(None,1)
            format_ls += [ (k,v)]
    meta['formatOption_ls'] = format_ls
    
    meta['itemsPerPageOption_ls'] = '1 2 5 10 20 50 100 200 500 1000 2000'.split()
    if (pageNumber - 1) * itemsPerPage > meta['totalResults']:
        pageNumber = 1
    startIndex = (pageNumber - 1)* itemsPerPage
    endIndex = startIndex + itemsPerPage
    data['records'] = records[startIndex:endIndex]  ## or get this set of records by a source-specific function
    meta['pageNumber'] = pageNumber
    meta['itemsPerPage'] = itemsPerPage
    meta['totalPages'] = meta['totalResults']/ itemsPerPage
    if meta['totalResults'] % itemsPerPage >0: meta['totalPages'] += 1
    data['metadata'] = meta
    return data



table_template = '''
        <!-- begin table segm container -->
        <div  >
        <!-- begin segm content -->
        <div>
        <!-- text content -->
        <div class="j">
        <table>
        $table_rows$
        </table>
        <!-- end text content -->
        </div>
        <!-- end segm content -->
        </div>
        <!-- end segm container -->    
        </section>
        <!-- end segm container ===================== -->
        '''
dl_template = '''
        <!-- begin template segm container -->
        <div  >
        <!-- begin segm content -->
        <div>
        <!-- text content -->
        <div class="j">
        <dl class="cvlike">
        $rows$
        </dl>
        <!-- end text content -->
        </div>
        <!-- end segm content -->
        </div>
        <!-- end segm container -->    
        </section>
        <!-- end segm container ===================== -->
        '''

def make_honor_rows(honor):
    d = honor
    link_honor = add_links(d['text'],global_vars['link_ls'])
    rows = '<dt>' + d['year'] + '</dt><dd>' + link_honor + '</dd>\n'
    if d.get('citation',''):
        rows += '<dt></dt><dd>&quot;' + d['citation']  + '.&quot;</dd>\n'
    return rows

def make_row(d): 
    text = d.get('text','')
    text = add_links(text, global_vars['link_ls'])
    return '<dt>' + d.get('year','') + '</dt><dd>' + text + '</dd>\n'

def make_images_html(d):
    name = d['complete_name']
    html = ''
    if d.get('Image',[]):
        link = d.get('Image',[])[0]   ## use only the first one
        href = link.get('href','')
        src = link.get('src','')
        if href and src:
            html += '<a href="' + href + '"> <img class="profilephoto" src="' + src + '" height="100px" alt="Profile - ' + name + '"></a>'
        return html
    return ''


def make_biblio_rows(b):
    return '<dt></dt><dd>' + link2html(b)+ '</dd>\n'

def make_bio_rows(b): 
    title = b.get('title','').strip()
    # Untitled works simply get NO TITLE
    if title == 'Untitled': title = ''
    author = b.get('author','').strip()
    # Anonymous works simply get NO AUTHOR
    if author == 'Anonymous': author = ''
    howpub  = b.get('howpublished','')
    year = b.get('year','')
    # Unknown dates are indicated as UNDATED
    if year == 'year?': year = 'Undated'
    ref = ''
    if title:  
        if not title[-1] in '?.!': title += '.'
        ref += '<t>' + title + '</t> '
    if author: ref += '<au>' + author + '</au>. '
    ref += howpub
    # Enhance globally interesting books
    book_link_ls = []
    books = global_vars['books']
    for bkey in books.keys():
        if ref.find(bkey) >= 0:
            ref = ref.replace(bkey,books[bkey]['ref'])
            book_link_ls = books[bkey].get('link_ls',[])
    #for t in tag_map.keys():
    #    ref = ref.replace(t,tag_map[t])
    ref += ' '
    for link in b.get('link_ls',[]) + book_link_ls:
            link = enhance_link(link)
            ref += link2html(link)
    return 'year={' + year + '}\n' + ref + '\n'


def honor_cmp(h,k):
    if h['text'] == k['text']:
        return cmp( h['year'], k['year'] )
    else:
        return cmp( h['text'], k['text'] )

def link2html(link):
    href = link.get('href','').strip()
    if not href: return ''
    anchor = link['anchor']
    link['title'] = link.get('title',link.get('href',''))
    link['target'] = link.get('target','_blank')
    return '<a class="bracketed" href="' + link['href'] + '" title="' + link['title'] + '" target="' + link['target'] + '">' + anchor + '</a>'

def link_honor(h):
    link = {}
    href = h.get('href','')
    if href: 
        link['href'] = href
        link['anchor'] = honor['text']
        return link2html(link)
    else: return h['text']
    #elif h['text'] in org_url.keys():
    #    link['href'] = org_url[h['text']]
    #    link['anchor'] = h['text']
    #    return link2html(link)
    #else:
    #    try: 
    #        pre,post = h['text'].split(',',1)
    #        if pre in org_url.keys():
    #            link['href'] = org_url[pre]
    #            link['anchor'] = pre
    #            return link2html(link) + ',' + post
    #    except: pass
    #return h['text']

def linkify(text):
    text1 = ' '.join(text.split())
    if text1 in org_url.keys():
        linkz = {}
        linkz['href'] = org_url[text1]
        linkz['anchor'] = text
        return link2html(linkz) 
    else: return text
        

def link_position(p):
    ll = linkify(p)
    if ll != p: return ll
    else: 
        llinks = [ linkify(ph) for ph in p.split(',') ]
        return ', '.join(llinks)


def read_section(section_txt):
    #1963 Ph.D. University of California, Berkeley
    #    http://genealogy.math.ndsu.nodak.edu/id.php?id=34373
    #        :thesis_title On Optimal Stopping
    txt = '\n'.join( [ line.strip() for line in section_txt.split('\n') ])
    d = {}
    subsecs = txt.split('\n:')
    toplines = subsecs[0]
    try: top_line,toplines = toplines.split('\n',1)
    except: 
        top_line = toplines
        toplines = ''
    d['top_line'] = top_line
    #d['link_lines'] = toplines
    d['link_ls'] = lines2link_ls(toplines)
    for subsec in subsecs[1:]:
            words = subsec.split()
            key = words[0]
            if len(words) > 1:
                val = subsec.split(None,1)[1]   ## keep newlines
            else: val = ''
            d[key] = val.strip()           ## last value rules, like BibTeX
            #if d.has_key(key): d[key] += [val]  
            #else: d[key] = [val]
    return d

def read_bibitem(section_txt):
    txt = '\n'.join( [ line.strip() for line in section_txt.split('\n') ])
    d = {}
    subsecs = txt.split('\n:')
    toplines = subsecs[0]
    try: top_line,toplines = toplines.split('\n',1)
    except: 
        top_line = toplines
        toplines = ''
    d['top_line'] = top_line
    d['bibtype'],d['id'] = d['top_line'].split()
    try: 
        d['ref'],linklines = toplines.split('\n',1)
        d['link_ls'] = lines2link_ls(linklines)
    except: 
        d['ref'] = toplines
        d['link_ls'] = []
    for subsec in subsecs[1:]:
            words = subsec.split()
            key = words[0]
            if len(words) > 1:
                val = subsec.split(None,1)[1]   ## keep newlines
            else: val = ''
            d[key] = val.strip()           ## last value rules, like BibTeX
            #if d.has_key(key): d[key] += [val]  
            #else: d[key] = [val]
    return d

def read_book(section_txt):
    txt = '\n'.join( [ line.strip() for line in section_txt.split('\n') ])
    d = {}
    subsecs = txt.split('\n:')
    toplines = subsecs[0]
    try: top_line,toplines = toplines.split('\n',1)
    except: 
        top_line = toplines
        toplines = ''
    d['top_line'] = top_line
    d['bibtype'],d['id'] = d['top_line'].split()
    top_line_ls = toplines.split('\n')
    d['title'] = top_line_ls[0]
    d['creator'] = top_line_ls[1]   ## au or editor. with (ed if editor)
    d['howpublished'] = top_line_ls[2]   
    d['year'] = top_line_ls[3]   
    linklines = '\n'.join(top_line_ls)[4:]
    d['link_ls'] = lines2link_ls(linklines)
    for subsec in subsecs[1:]:
            words = subsec.split()
            key = words[0]
            if len(words) > 1:
                val = subsec.split(None,1)[1]   ## keep newlines
            else: val = ''
            d[key] = val.strip()           ## last value rules, like BibTeX
            #if d.has_key(key): d[key] += [val]  
            #else: d[key] = [val]
    d['ref'] = '<t>' + d['title'] + '</t>. ' 
    if d.has_key('edition'): d['ref'] += '(' + d['edition'] + ' edition). '
    d['ref'] += d['creator'] + '. ' 
    d['ref'] += d['howpublished'] + '. ' 
    return d

def read_4line_bibitem(section_txt):
    txt = '\n'.join( [ line.strip() for line in section_txt.split('\n') ])
    d = {}
    subsecs = txt.split('\n:')
    toplines = subsecs[0]
    try: top_line,toplines = toplines.split('\n',1)
    except: 
        top_line = toplines
        toplines = ''
    d['top_line'] = top_line
    try: 
        d['bibtype'],d['id'] = d['top_line'].split()
    except:
        print 'Error parsing: ' + d['top_line'] 
    toplines = toplines.split('\n')
    d['title'] = toplines[0]
    try: 
        d['author'] = toplines[1]
        d['howpublished'] = toplines[2]
        d['year'] = toplines[3]
    except: 
        print 'Error parsing:'
        print toplines
    linklines = '\n'.join(toplines[3:])
    d['link_ls'] = lines2link_ls(linklines)
    for subsec in subsecs[1:]:
            words = subsec.split()
            key = words[0]
            if len(words) > 1:
                val = subsec.split(None,1)[1]   ## keep newlines
            else: val = ''
            d[key] = val.strip()           ## last value rules, like BibTeX
            #if d.has_key(key): d[key] += [val]  
            #else: d[key] = [val]
    return d

def read_degree(degree_txt):
    #1963 Ph.D. University of California, Berkeley
    #    http://genealogy.math.ndsu.nodak.edu/id.php?id=34373
    #        :thesis_title On Optimal Stopping
    d = read_section(degree_txt)
    d['category'] = 'degree'
    try: d['year'],rest = d['top_line'].split(None,1)
    except: 
        d['year'] = d['top_line']
        rest = ''
    try: d['type'],rest = rest.split(None,1)
    except: 
        d['type'] = rest
        rest = ''
    d['school'] = rest
    del d['top_line']
    return d

def read_generic(txt):
    d = read_section(txt)
    try: 
        d['year'],rest = d['top_line'].split(None,1)
        d['year'] = d['year'].replace('_',' ')
    except: 
        d['year'] = ''
        rest = d['top_line']
    d['text'] = rest
    del d['top_line']
    return d

def read_education(txt):
    d = read_generic(txt)
    d['category'] = 'education'
    return d

def read_service(txt):
    d = read_generic(txt)
    d['category'] = 'service'
    return d

def read_member(txt):
    d = read_section(txt)
    d['category'] = 'member'
    d['text'] = d['top_line']
    del d['top_line']
    return d

def read_image(txt):
    d = read_section(txt)
    del d['link_ls']    ## all bare urls expected in the top_line
    d['category'] = 'image'
    words = d['top_line'].split()
    hrefs = [ w for w in words if w[0:4] == 'http']
    textwords  = [ w for w in words if not w[0:4] == 'http']
    if hrefs:
        d['src'] =  hrefs[0]
        if len(hrefs) == 1:      ## href and src are identical
            d['href'] =  hrefs[0]
        elif len(hrefs) > 1:
            d['href'] =  hrefs[1]
            ## ignore if more than 2 urls
    d['text'] = ' '.join(textwords)
    del d['top_line']
    return d

def read_homepage(txt):
    d = read_section(txt)
    del d['link_ls']    ## all bare urls expected in the top_line
    d['category'] = 'homepage'
    d['rel'] = 'homepage'
    words = d['top_line'].split()
    hrefs = [ w for w in words if w[0:4] == 'http']
    textwords  = [ w for w in words if not w[0:4] == 'http']
    if hrefs:
        if len(hrefs) >= 1:      ## href 
            d['href'] =  hrefs[0]
            ## ignore if more than 2 urls
    d['anchor'] = ' '.join(textwords)
    del d['top_line']
    #print json.dumps(d)
    return d

def read_honor(txt):
    d = read_generic(txt)
    d['category'] = 'honor'
    return d

def read_position(txt):
    d = read_generic(txt)
    d['category'] = 'position'
    return d

def read_bio(txt):
    #d = read_bibitem(txt)
    d = read_4line_bibitem(txt)
    return d

def enhance_link(link):
        rel = link.get('rel','')
        if link['href'].find('mathscinet') >= 0:
            link['anchor'] = 'MathSciNet'
            link['rel'] = 'biblio'
            link['status'] = 'top'
        elif link['href'].find('academic.research.microsoft.com') >= 0:
            if not link.get('anchor','').find('Microsoft Academic:') >= 0:
                link['anchor'] = 'Microsoft Academic: ' + link.get('anchor','')
            link['rel'] = 'biblio'
        elif link['href'].find('scholar.google') >= 0:
            link['anchor'] = 'Google Scholar'
            link['rel'] = 'biblio'
            link['status'] = 'top'
        elif link['href'].find('celebratio') >= 0:
            link['anchor'] = 'Celebratio'
            link['rel'] = 'biblio'
            link['status'] = 'top'
        elif link['href'].find('zbmath') >= 0:
            link['anchor'] = 'zbMATH'
            link['rel'] = 'biblio'
            link['status'] = 'top'
        elif rel.find('pubspage') >= 0:
            link['anchor'] = 'Publication List'
            link['rel'] = 'biblio'
        elif rel.find('homepage') >= 0:
            link['anchor'] = 'Homepage'
            link['rel'] = 'homepage'
            link['status'] = 'top'
        elif rel.find('bookspage') >= 0:
            link['anchor'] = 'Books List'
            link['rel'] = 'biblio'
        elif link['href'].find('genealogy.math') >= 0:
            link['anchor'] = 'Math. Genealogy'
            link['rel'] = 'educ'
        elif link['href'].find('wikipedia') >= 0:
            link['anchor'] = 'Wikipedia'
            link['rel'] = 'bio'
            link['status'] = 'top'
        else:
            link['rel'] = 'misc'
            anchor = link.get('anchor','').strip()
            if not anchor:
                link['anchor'] = link['href'].split('/')[2]
        return link

"""
This collection of functions adds the individual subsections of the LaTeX doc.

Main sections are:
  Education, Career, Honors, Professional Service, Membership, and Bibliography.

There are additional sections for publication-like data:
  Biographies, Symposia, Archives, Art_Exhibitions, Collected_Works, Selected_Works, DVDs,
  Endowments, Festschriften, Memoirs, Oral_History, Death_Notices, Obituaries, Memorials

This part is handled by  bio_latex  and  biblio_latex,  which
generate both BibTeX to include via filecontents, and
in-line references to these bibliographic items.
"""

#encode education as latex
def educ_latex(person):
    educ = person.get('Education',[]) + person.get('Degree',[])
    if not educ: return ''
    #educ.sort(year_cmp)
    heading = '\n\n\\subsection*{Education}\n'
    rows = ''
    for d in educ:
        if d['category'] == 'degree':
            award_kind = '\\Degree'
            award_type = '{' + d['type'] + '}'
        #don't need type for education rows
        elif d['category'] == "education":
            award_kind = '\\Education'
            award_type = ''
            d['school'] = d['text']
            
        d['text'] = d.get('type','')  + ', ' + d.get('school','')  + ' '  ## could hyperlink here
        rows += award_kind + '{' + d['year'].replace(u'–','--') + '}' + award_type + '{' + sanitize_latex(d.get('school','')) + '}'

        #print optional elements (e.g. thesis title)
        if d.get('thesis_title','').strip():
            rows += '{' + sanitize_latex(d['thesis_title']) + '}'
        #if d.get('link_ls',''):
            #rows += '{' + d.get['link_ls'] + '}'
        for link in d['link_ls']:
            if link['href'].find('genealogy') >= 0:
                rows += '{' + link['href'] + '}'
        rows += '\n'
    #print heading + rows
    return heading + rows

def career_latex(person):
    #[{'category': 'position', 'text': u'Department of Statistics, University of Melbourne', 'year': u'19??-1982', 'link_ls': []}]
    career = person.get('Position',[])
    if not career: return ''
    heading = '\n\n\\subsection*{Career}\n'
    rows = ''
    for d in career:
        text = d['text'].split(',',1)
        #links???
        rows +='\\Position{' + d['year'].replace(u'–','--') + '}{' + sanitize_latex(text[0]) + '}{' + sanitize_latex(text[-1]) + '}\n'
    return heading + rows

def honors_latex(person):
    #[{'category': 'honor', 'text': u'IMS Fellow', 'year': u'before 1943', 'link_ls': []}]
    honors = person.get('Honor',[])
    #either Honor or Honorary Degree, Honorary Degree indicated by presence of (honorary)
    if not honors: return ''
    heading = '\n\n\\subsection*{Honors}\n'
    rows = ''
    for d in honors:
        text = d['text']
        if '(Honorary)' in text:
            text1 = text.split('(')
            text2 = text.split(')')
            rows += '\\HonoraryDegree{' + d['year'].replace(u'–','--') + '}{' + sanitize_latex(text1[0]) + '}{' + sanitize_latex(text2[-1].strip()) + '}\n'
        else:
            rows += '\\Honor{' + d['year'].replace(u'–','--') + '}{' + sanitize_latex(d['text']) + '}\n'
    return heading + rows

def service_latex(person):
    service = person.get('Service',[])
    if not service: return ''
    heading = '\n\n\\subsection*{Professional Service}\n'
    rows = ''
    for d in service:
        text = d['text'].split(',')
        rows += '\\Service{' + d['year'].replace(u'–','--') + '}{' + sanitize_latex(text[0]) + '}{' + sanitize_latex(text[-1].strip()) + '}\n'
    return heading + rows

def member_latex(person):
    member = person.get('Member',[])
    if not member: return ''
    heading = '\n\n\\subsection*{Membership}\n'
    rows = ''
    for d in member:
        rows += '\\Member{' + sanitize_latex(d['text']) + '}\n'
    return heading + rows

# Still to fix
def biblio_latex(person):
        heading = '\n\n\\subsection*{Bibliography}\n'
        rows = ''
        for b in person.get('link_ls',[]):
            bb = enhance_link(b)
            if bb.get('rel','') == 'biblio':
                rows += make_biblio_rows(bb)
        return rows

def source_data_html(person):
    templ = '''<h4 class="alt js-collapse js-collapseoff">Source Data</h4>
    <div class="collapsed-region">
    <pre>$text$</pre>
    </div>'''
    h = templ.replace('$text$',person['public_record_txt'])
    return h

# The fact that we're getting unicode here is perhaps a bit of a problem
# TO FIX
def bio_latex(person):
    citations = ''
    name = person['complete_name']
    localized = open("./bibfiles/" + name + '.bib', 'w')
    comment = "%% BibTeX file for " + name
    localized.write(comment.encode('utf-8'))
    localized.close()
    for c in bio_cat_order[0:]:
        bios = person.get(c,[])
        if not bios: continue
        elif len(bios) == 1:
            heading = '\n\n\\subsection*{' + c.replace('_',' ') + '}\n'
        elif len(bios) > 1:
            heading = '\n\n\\subsection*{' + bio_cat_plural[c].replace('_',' ') + '}\n'
        rows = ''
        cites = ''
        bios.sort(year_cmp)
        for b in bios:
            #print b
            if b['bibtype'] == "webcollection":
                btype = collection
            else:
                btype=b['bibtype']
            rows += '\n\n@' + btype + '{' + b['id'] + ',\n'
            rows += 'year={' + b['year'] + '},\n'
            rows += 'author={' + sanitize_latex(b['author']) + '},\n'
            rows += 'title={' + sanitize_bibtex(sanitize_latex(b['title'])) + '},\n'
            # we've need to read the howpublished field and refactor the entries
            rows += read_howpublished(b['howpublished'])
            rows += '}'
            cites += "\\" + c.replace('_','') + '{' + b['id'] + '}\n'
        citations += heading + cites
        # Write out bibtex to a file we will reuse later
        name = person['complete_name']
        localized = open("./bibfiles/" + name + '.bib', 'a')
        localized.write(rows.encode('utf-8'))
        localized.close()
        print "added to bib file: " + name.encode('utf-8') + ".bib"
        # And just for ease of checking, append ALL the bibtex here
        unified=open("allbib.bib", "a")
        unified.write(rows.encode('utf-8'))
        unified.close()
    return citations

# Note: it's problematic to introduce title AGAIN if we already have one, what to do?
def read_howpublished(howpubinfo):
    keytag= [["address", "address"],
             ["au", "author"],
             ["author",  "author"],
             ["booktitle", "booktitle"],
             ["bt", "BIB-TITLE"],        # These are not in bibtex but rather are references
             ["cit", "BIB-CITATION"],    # to something else - but none appear in output, so...
             ["ed", "editor"],
             ["howpub", "note"],         # nested howpubs are dealt with as notes
             ["howpublished", "note"],   #
             ["note", "note"],   
             ["j", "journal"],
             ["journal", "journal"],
             ["pages", "pages"],
             ["pp", "pages"],
             ["pub", "publisher"],
             ["publisher", "publisher"],
             ["se", "series"],
             ["series", "series"],
             ["t", "title"],
             ["title", "title"],
             ["v", "volume"],
             ["vol", "volume"],
             ["volume", "volume"],
             ["n", "number"],
             ["number", "number"],
             ["webcollection", "booktitle"],
             ["y", "year"],
             ["year", "year"]]
    retval=''
    for elt in keytag:
        bounded_expression = re.compile("<" + elt[0] + ">(.+?)</" + elt[0] +">" )
        match = re.search(bounded_expression,howpubinfo)
        if match :
            retval += elt[1] + "={" + sanitize_latex(match.group(1).strip()) + "},\n"
            if (elt[1]=="title" or elt[1]=="booktitle") :
                retval = sanitize_bibtex(retval)
    # deal with cross-references to items collected in imsBooks.bib
    match= re.search("<rel>In </rel><inc>(.+?)</inc>",howpubinfo)
    if match :
        retval += "crossref={" + match.group(1).strip() + "},\n"
    return retval

def make_mg_data(data):
    p = ''
    mg2ims = {}
    ims2mg = {}
    ims2mg_txt = {}
    urls = []
    for d in data['records']:
        for link in d['link_ls']:
            if link['href'].find('genealogy') >= 0:
                mg2ims[ link['href'] ] = d['id']
                urls += [link['href']]
    mgrecords = math_genealogy_api.get_items_by_id(urls)
    for i in range(len(urls))[0:]:
        u = urls[i]
        r = mgrecords[i]
        ims2mg[ mg2ims[u] ] = r
    items = []
    for k in ims2mg.keys():
        r = ims2mg[ k ]
        p =  ':: ' +  k + '\n'
        mgurl = ims2mg[k]['id'].replace('math_genealogy_author:','http://genealogy.math.ndsu.nodak.edu/id.php?id=')
        p += ':Degree ' + r.get('degree_year','?year?') + ' ' + r.get('degree_type','?type?') + ' ' + r.get('degree_school','?school?') + '\n\t' +  mgurl + '\n' 
        p += '\t:thesis_title ' + ' '.join( r.get('thesis_title', '').split() ) + '\n'
        ims2mg_txt[k] = p
        #items += [p]
    #items.sort()
    #p = '\n'.join(items) + '\n'
    #outfile = open('degree_data.txt','w')
    #outfile.write(p.encode('utf-8'))
    #outfile.close()
    return ims2mg,ims2mg_txt

def year_test(txt):
    if len(txt) != 4: return False
    try:
        txt  = str(int(txt))
        if txt[0:2] in '18 19 20'.split(): return True
        else: return False
    except:  return False

def add_mg_data():
    data = read_ims_legacy('ims_legacy_0')
    ims2mg,ims2mg_txt = make_mg_data(data)
    p = data['metadata']['record_txt']
    p += '\n'
    for d in data['records']:
        r = d['record_txt']
        r = r.replace(':Honor \n',':Honor  ')   ##  to be deprecated soon
        r = r.replace(':Honor\n',':Honor  ')   ##  to be deprecated soon
        r = r.replace(':Honor  \n',':Honor  ')   ##  to be deprecated soon
        p += r
        degree_text = ims2mg_txt.get(d['id'],'')
        try: degree_text = degree_text.split(':Degree',1)[1].strip()
        except: degree_text = ''
        words = degree_text.split()
        if words:
            y = words[0]
            if not year_test(y): 
                if not y == '?year?':
                    degree_text = '?year? ' + degree_text
            degree_text = ':Degree ' + degree_text
        p += degree_text
        p += '\n\n'
    p = p.encode('utf-8')
    outfile = open('xxims_legacy.txt','w')
    outfile.write(p)
    outfile.close()
    #print p

def add_microsoft_data():
    data = read_ims_legacy('ims_legacy_14')
    #import microsoft_academic_api
    #microsoft_data = microsoft_academic_api.read_dict()
    p = data['metadata']['record_txt']
    for d in data['records']:
        addtxt = ''
        for link in d['link_ls']:
            if link['href'] in microsoft_data.keys():
                md = microsoft_data[link['href']]
                src_url = md.get('microsoft_photo_url','')
                ph_url = md.get('photo_url','')
                home_url = md.get('homepage_url','')
                if home_url: 
                    addtxt += ':Homepage ' + home_url + '\n'
                if src_url:
                    addtxt += ':Image ' + src_url + ' ' 
                if ph_url:
                    addtxt += ph_url  + '\n'
        pre,post = d['record_txt'].split('\n:Honor',1) 
        p += '\n' + pre + '\n' + addtxt + ':Honor' + post
    outfile = open('ims_legacy.txt','w')
    outfile.write(p.encode('utf-8'))
    outfile.close()
    
def add_bio_data():
    data = read_ims_legacy('ims_legacy_3')
    bios = open('items/biographies.txt')
    t = bios.read()
    misc = open('items/misc.txt')
    t += misc.read()
    obits = open('items/obituaries.txt')
    t += obits.read()
    #t = unicode(t,'utf-8')
    t = '\n' + t.strip()
    items = t.split('\n::')[1:]
    bios = {}
    for item in items[1:]:
        lines = item.split('\n')
        lines = [ json.loads('"' + line + '"') for line in lines ]
        lines = ['\t' + line for line in lines ]
        try: 
            cat, ii = lines[-2].split()
        #bios[ii] = bios.get(ii,'') + ':Biography ' + '\n'.join(lines[0:-2]) + '\n'
            bios[ii] = bios.get(ii,'') + ':' + cat.split('_of')[0].replace('@','')  + ' ' +  '\n'.join(lines[0:-2]) + '\n'
        except: print lines
    #for ii in bios.keys():
    #    print bios[ii].encode('utf-8')
    p = data['metadata']['record_txt']
    p += '\n'
    for d in data['records']:
        r = d['record_txt']
        p += r
        bio_txt = bios.get(d['id'],'')
        p += bio_txt
        p += '\n\n'
    p = p.encode('utf-8')
    outfile = open('ims_legacy.txt','w')
    outfile.write(p)
    outfile.close()
    #print p

def make_dates_html(d):
    templ = '<p id="lifespan">DOB&thinsp;&ndash;&thinsp;DOD</p>'
    if d.has_key('DOB') and d.has_key('DOD'):
        for k in 'DOB DOD'.split(): templ = templ.replace(k, show_date( getf(d,k) ) )
        return templ 
    else: return ''

def make_dates_plain_html(d):
    templ = 'DOB&nbsp;-&nbsp; DOD<br>'
    if d.has_key('DOB') and d.has_key('DOD'):
        for k in 'DOB DOD'.split(): templ = templ.replace(k, show_date( getf(d,k) ) )
        return templ 
    else: return ''

def top_links_html(d):
    html = ''
    for link in d.get('link_ls',[]) + d.get('Homepage',[]):
        link = enhance_link(link)
        if link.get('status','') == 'top':
            html += link2html(link)
    return html

def first_first(name):
    last,first = name.split(',',1)
    return first.strip() + ' ' + last.strip()

def add_latex(d):
        content = '' 
        content += educ_latex(d)
        content += career_latex(d)
        content += honors_latex(d)
        content += service_latex(d)
        content += member_latex(d)
        
        #JOE
        content += bio_latex(d)
        #content += biblio_latex(d)
        d['latex'] = content
        return d

def make_all():
    # For testing purposes, I'm creating a file with all of the bib data
    unified=open("allbib.bib", "w")
    unified.write("%% COMMENT This is a collection of all the bibliographic data\n\n")
    unified.close()
    out_dir = global_vars['published_files_directory'] 
    infile = open('./celebratio_cv_template.html')
    html = infile.read()
    html = unicode(html,'utf-8')

    data = read_ims_legacy('ims_legacy')
    print 'Read ' + str(len(data['records'])) + ' records from ims_legacy.txt'
    global_vars['link_ls'] = data['link_ls']
    global_vars['books'] = data['books']
    records = [ add_latex(d) for d in data['records'] ]
    tot = len(records)
    print 'Making xml for ' + str(tot) + ' records'
    make_xml( records)

    for d in records:
        content = ''
        name = d['complete_name']

        bibcontent = ''
        try:
            bibfile = open("./bibfiles/" + name + '.bib', 'r')
            bibcontent = unicode(bibfile.read(),'utf-8')
            bibfile.close()
        except: continue

        content +=  global_vars['latex_beg'] + bibcontent + global_vars['latex_med'] + d['latex'] + global_vars['latex_end']

        filename = name + '.tex'
        f = open("./texfiles/" + filename, 'w')
        f.write(content.encode('utf-8'))
        f.close()
        print "made new latex file: " + filename.encode('utf-8')

# This will fix the typical characters that cause errors in LaTeX articles
# Should double check that this is always what's wanted, e.g. in the case of underscores
# which could be used in mathematical expressions to denote subscripts
def sanitize_latex(txt):
    # Replace accent marks
    char_array = list(latex_accents.replace_html_accents(txt).decode('utf-8'))
    # Replace common ASCII-isms with corresponding LaTeX-isms
    i = 0
    while i < len(char_array):
        if re.match("(&|#|_)",char_array[i]) and (i == 0 or char_array[i-1] != "\\") :
            char_array[i] = "\\" + char_array[i] 
        elif char_array[i] == u"‘":
            char_array[i] = u'`'
        elif char_array[i] == u"’":
            char_array[i] = u"'"
        i=i+1
        # print char_array[i].encode("utf-8")
    return "".join(char_array)

# Replace every Capital Letter Except The First with a Bracketed Version!
# Replace every {C}apital {L}etter {E}xcept {T}he {F}irst with a {B}racketed {V}ersion!
def sanitize_bibtex(txt):
    char_array = list(txt)
    i = 0
    while i < len(char_array) :
        if re.match("[A-Z`']",char_array[i]) and (i == 0 or char_array[i-1] != "{") and (i == len(char_array) -1 or char_array[i+1] != "}"):
            char_array[i] = "{" + char_array[i] + "}"
        i=i+1
#    if (char_array[len(char_array)-1] == "`" or char_array[len(char_array)-1] == "`")
#        char_array[len(char_array)-1] = "{" + char_array[len(char_array)-1] + "}"
    return "".join(char_array)

def enhance_bio(d):
    ref = d['ref']
    ref = ref.replace('author>','au>')
    ref = ref.replace('year>','y>')
    ref = ref.replace('journal>','j>')
    ref = ref.replace('title>','t>')
    ref = ref.replace('bt>','t>')
    try: 
        ayt, howpublished = ref.split('</t>',1)
        howpublished = ' '.join(howpublished.split())
        if howpublished[0] == '.':
            howpublished = howpublished[1:].strip()
        d['howpublished'] = howpublished
    except: 
        d['howpublished'] = ref
    
    try: title = ref.split('<t>',1)[1].split('</t>')[0].strip()
    except: title = ''
    if title: d['title'] = title
    else: d['title'] = 'Untitled'
    try: author = ref.split('<au>',1)[1].split('</au>')[0].strip()
    except: author = ''
    if author:  d['author'] = author
    else: d['author'] = 'Anonymous'
    try: year = ref.split('<y>',1)[1].split('</y>')[0].strip()
    except: year = ''
    if not year:
        try: year = ref.split('(',1)[1].split(')')[0]
        except: year = ''
    if not year: year = get_year_from_str(ref)
    if year: d['year'] = year
    else: d['year'] = 'year?'
    return d
    
def parse(text,category):
    #data = read_ims_legacy('ims_legacy_6')
    bios = text.split(':' + category)
    p = bios[0]
    for b in bios[1:]:
        try: 
            b,rest = b.split('\n:',1)
            rest = '\n:' + rest
        except: rest = ''
        d = read_bibitem(b)
        d = enhance_bio(d)
        t = ''
        t += ':' + category + ' ' + d['top_line'] + '\n'
        t += '\t' + ' '.join(d.get('title','Untitled').split()) + '\n'
        t += '\t' + ' '.join(d.get('author','Anonymous').split()) + '\n'
        t += '\t' + ' '.join(d.get('howpublished','howpublished?').split()) + '\n'
        t += '\t' + ' '.join(d.get('year','year?').split()) + '\n'
        for link in d.get('link_ls',[]):
            t += '\t' + link['href'] + ' ' + link.get('anchor','') + '\n'
        t+= '\t:ref ' + d['ref'] + '\n'
        p += t
        p += rest
    return p

def parse_all():
    categories = '''
    Biography
    Archive
    Art_Exhibition
    Collected_Works
    DVD
    Endowment
    Festschrift
    Memoir
    Oral_History
    Selected_Works
    Symposium
    Death_Notice
    In_Memoriam
    Obituary
    '''.split()
    infile = open('ims_legacy_7.txt')
    txt = infile.read()
    txt = unicode(txt, 'utf-8')
    for c in categories[0:]:
        txt = parse(txt,c)
    txt = txt.encode('utf-8')
    outfile = open('xxims_legacy.txt','w')
    outfile.write(txt)
    outfile.close()

def missing_emails():
    data = read_ims_legacy()
    for d in data['records'][0:]:
        if not d.get('Deceased',[]):
            if not d.get('Email',[]):
                print d['record_txt'].encode('utf-8')


if __name__ == '__main__':
    make_all()
    publish_ims_legacy()
    #missing_emails()
    
