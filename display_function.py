## default display function capabilities
import json
import urllib
#import accents

def make_links(r):
    links = []
    if r.has_key('mrnumber'):
        link = {}
        link['href'] = 'http://www.ams.org/mathscinet-getitem?mr=' + r['mrnumber'].split()[0]
        links += [link]
    if r.has_key('doi'):
        link = {}
        link['href'] = 'http://dx.doi.org/' + r['doi']
        links += [link]
    if r.has_key('url'):
        if not r['url'] == 'http://dx.doi.org/' + r.get('doi',''):
            link = {}
            link['href'] = r['url']
            links += [link]
    if 1:
        link = {}
        q = 'author:"' + r.get('author','').split(' and ')[0] + '"' + r.get('title','')
        passd={}
        passd['q'] = q.encode('utf-8')
        link['href'] = 'http://scholar.google.com/scholar?' + urllib.urlencode(passd)
        link['anchor'] = 'Google Scholar'
        links += [link]

    note = r.get('note','')
    if note.lower().find('arxiv:') >= 0:
        arxid = note.lower().split('arxiv:',1)[1].strip()
        link = {}
        link['href'] = 'http://arxiv.org/abs/' + arxid
        links += [link]
    return links


def link2html(link):
    h = ''
    #return json.dumps(link,indent=4)
    url = ''
    title = ''
    anchor = ''
    url = link['href'].strip()
    anchor = link.get('anchor','').strip()
    if not anchor:
	    if url.find('http://zbmath.org/?q=an:') >= 0:
		    anchor = 'zbMATH'
		    title = 'zbMATH an:' + url.split('http://zbmath.org/?q=an:',1)[1]
	    elif url.find('http://www.ams.org/mathscinet-getitem?mr=') >= 0:
		    anchor = 'MR'
		    title = 'MathSciNet MR' + url.split('http://www.ams.org/mathscinet-getitem?mr=',1)[1]
	    elif url.find('http://dx.doi.org/') >= 0:
		    anchor = 'DOI'
		    title = 'DOI: ' + url.split('http://dx.doi.org/',1)[1]
	    elif url.find('www.ams.org/journal-getitem') >= 0:
		    anchor = 'AMS'
		    title = url
	    elif url.find('math-doc') >= 0:
		    anchor = 'MathDoc'
		    title = url
	    elif url.find('link.springer.com') >= 0:
		    anchor = 'SpringerLink'
		    title = url
	    elif url.find('www.springer.com') >= 0:
		    anchor = 'SpringerBooks'
		    title = url
	    elif url.find('http://arxiv.org/abs/') >= 0:
		    anchor = 'arXiv'
		    title = 'arXiv: ' + url.split('http://arxiv.org/abs/',1)[1]
	    elif url.find('projecteuclid') >= 0:
		    anchor = 'Project Euclid'
		    title = url
	    elif url.find('numdam') >= 0:
		    anchor = 'NUMDAM'
		    title = url
	    elif url.find('http://arxiv.org/pdf/') >= 0:
		    anchor = 'arXiv: pdf'
		    title = 'arXiv: ' + url.split('http://arxiv.org/pdf/',1)[1] + 'pdf'
	    elif url.split('.')[-1] in 'pdf PDF'.split():
		    anchor = 'pdf'
		    title = url
	    elif url.find('ejpecp') >= 0:
		    anchor = 'ejpecp: ' + url.split('.')[-1]
		    title = url
	    elif url.find('http://dx.doi.org/') >= 0:
		    anchor = 'DOI'
		    title = 'DOI: ' + url.split('http://dx.doi.org/',1)[1]
	    elif url.split('.')[-1] in 'html htm HTML HTM'.split():
		    anchor = 'html'
		    title = url
	    else: 
		    anchor = link.get('anchor','')
            if not anchor: 
                anchor = url.split('/')[2]
            title = url
    if url: 
	    h =  '[<a href="' + url + '" title="' + title + '" target="link">' + anchor + '</a>]'
    else:   h = '[' + link['anchor']  + ']' 
    return h

def editor_text(passd):
    etext = passd.get('editor','').strip()
    if not etext: return ''
    else:
        eds = etext.split(' and ')
        if len(eds) == 1:
            etext = etext + ' (ed.)'
        else:
            etext = etext + ' (eds.)'
    return etext


def add_same_page_cites(txt):
    """ convert BibTeX \cite{xxx} to hyperlinks. This is tricky. Are they in the same page or not? BibServer should modify links on display accordingly """
    ss = txt.split('\\cite{')
    h = ss[0]
    for frag in ss[1:]:
        try: 
            k,v = frag.split('}',1)
        except:
            k = ''
        if k:
            h += '[<a href="#' + k + '">' + k + '</a>]'  + v
        else: h += frag
    return h
    
def howpublished_tagged(r):
            howpub = r.get('howpublished','')
            if not howpub:
                passd = {}
                passd.update(r)
                if passd.get('journal',''): passd['journal']  = '<j>' + passd['journal'] + '</j>'
                if passd.get('volume',''): passd['volume']  = 'Vol. <v>' + passd['volume'] + '</v>'
                if passd.get('pages',''): passd['pages']  = 'pp.<pp>' + passd['pages'] + '</pp>'
                if passd.get('booktitle',''): passd['booktitle']  = 'In: ' + '<bt>' + passd['booktitle'] + '</bt>'
                vv = [ passd.get(k,'').strip() for k in 'journal booktitle editor series publisher volume number pages note'.split() ]
                vv = [ v for v in vv if v ]
                try: howpub = vv[0]
                except: howpub = '???'
                for v in vv[1:]:
                    try: howpub += ', ' + v
                    except: howpub += ', ' + '????'
            return howpub
def howpublished_plain(r):
            howpub = r.get('howpublished','')
            if not howpub:
                passd = {}
                passd.update(r)
                if passd.get('booktitle',''): passd['booktitle']  = 'In: ' + passd['booktitle'] 
                if passd.get('editor',''): 
                    eds = passd.get('editor','').split(' and ')
                    if len(eds) == 1:
                        passd['editor']  = '(' + passd['editor'] + ' ed.)'
                    else:
                        passd['editor']  = '(' + passd['editor'] + ' eds.)'
                vv = [ passd.get(k,'').strip() for k in 'journal booktitle editor series publisher volume number pages note'.split() ]
                vv = [ v for v in vv if v ]
                try: howpub = vv[0]
                except: howpub = '???'
                for v in vv[1:]:
                    try: howpub += ', ' + v
                    except: howpub += ', ' + '???'
            return howpub
        
def display_html(r):
            ii = r.get('id','')
            h = '[<a name="' + ii + '">' + ii + '] '
            h += r.get('author','')
            if not h: h = r.get('editor','') + '(ed.)'
            year = r.get('year','')
            if year:  h += ' (' + year + ')'
            h += '<br>'
            h += '<strong>' + r.get('title','') + '</strong> <br>'
            howpub = r.get('howpublished','')
            if not howpub:
                if r.get('journal',''): r['journal']  = '<i>' + r['journal'] + '</i>'
                if r.get('volume',''): r['volume']  = '<strong>' + r['volume'] + '</strong>'
                vv = [ r.get(k,'').strip() for k in 'journal booktitle series publisher volume number pages'.split() ]
                vv = [ v for v in vv if v ]
                try: howpub = vv[0]
                except: howpub = '???'
                for v in vv[1:]:
                    try: howpub += ', ' + v
                    except: howpub += ', ' + '????'
            try: h += howpub 
            except: h += '???'
            h+= '<br>'
            note = r.get('note','').strip()
            if note: 
                if not note[-1] in '.?,;:': note = note + '.'
                h += add_same_page_cites(note)
            for link in r.get('link_ls',[]) + make_links(r):
                h += link2html(link)
            return h ## accents.tex2utf8(h)

def display_function(display_style,r):
        """function for a record into one line of an html table for display"""
        if display_style == 'howpublished_plain':
            return howpublished_plain(r)
        elif display_style == 'howpublished_tagged':
            return howpublished_tagged(r)
        elif display_style == 'two_lines':
            p = '<td>' 
            p += '<strong>' + r.get('title','') + '</strong>.<br>'
            p += r.get('author','') + ' '
            eds = r.get('editor','')
            if eds: 
                p += r.get('editor','') + ' (ed.)'
            p += '(' + str(r.get('year','')) + '). '    ## may get None?
            bibtype = r.get('bibtype','')
            if bibtype == 'book':
                p += r.get('publisher','') + ' '
            elif bibtype == 'article':
                p += r.get('journal','') + ' '
            elif bibtype == 'chapter':
                p += 'In: ' + r.get('booktitle','') + '. '
            for link in r.get('link_ls',[]):
                p += link2html(link)
            p += '</td>'
            return p
        elif display_style == 'item_html':  return r.get('item_html','') + '<hr>'
        elif display_style == 'bibtex':  
            return '<pre>' + r.get('bibtex','') + '</pre>'
        elif display_style == 'html':  return display_html(r) + '<hr>'
        elif display_style == 'abstracts':
            h = display_html(r)
            if r.has_key('abstract'):
                h += '<br><strong>Abstract:</strong> ' + r['abstract'] 
            h += '<hr>'
            return h
        elif display_style == 'json_display':  
            return '<pre>' + json.dumps(r,indent=4) + '</pre>'
        elif display_style == 'one_line':  
            return r['title'] + '. (' + r['year'] + '). ' + r['title']  + '<br>'
        else: 
            return str(display_style) +  ': unknown display style' + '<br>'
    
