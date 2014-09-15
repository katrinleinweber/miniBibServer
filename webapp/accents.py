#this Python file uses the following encoding: utf-8
## http://www.ams.org/membership/texcodes

import unicodedata

import HTMLParser
hparser  = HTMLParser.HTMLParser()
## for hparser.unescape()


import os
accents_fname = os.path.join(os.path.dirname(__file__), "accents.txt")  
# so accents_txt is the name of the file "accents.txt" in the same directory as this code file
accents_txt = open(accents_fname).read()
accents_uni = unicode(accents_txt,'utf-8')

def uni2ascii(text):
    asc = ''
    for char  in text: 
        try: asc += unicodedata.normalize('NFKD', char ).encode('ascii', 'ignore')
        except: asc += char
    return asc

def make_utf8_to_tex():
    d = {}
    lines = accents_uni.split('\n')
    for line in lines:
        if line:
            k,v = line.split(None,1)
            d[k] = v
    return d


def xconvert(txt,dictionary):
    for k,v in dictionary.items():
        txt = txt.replace(k,v)
    return txt

def convert(txt,dictionary):  ## need patch for $$
    txt = txt.replace('\\$','\\dollarsign')
    ss = txt.split('$')
    p = ''
    while ss:
        newtxt = ss[0]
        for k,v in dictionary.items(): newtxt = newtxt.replace(k,v)
        #newtxt = newtxt.replace('{','')
        #newtxt = newtxt.replace('}','')
        newtxt = newtxt.replace('\\&','&')
        p += newtxt
        if len(ss) > 1:
            p += '$' + ss[1] + '$'  ## hopefully matching $
        ss = ss[2:]
    p = p.replace('\\dollarsign','\\$')
    return p

def make_tex_to_utf8():
    d = {}
    lines = accents_uni.split('\n')
    for line in lines:
        if line.strip():
            k,v = line.strip().split(None,1)
            d[v] = k
            d[v[0:-1]+'{' + v[-1] + '}'] = k
    return d

tex2utf8_dict  = make_tex_to_utf8()
    
def tex2utf8(txt):
    txt = convert( txt, tex2utf8_dict)
    return txt

def txt2utf8(txt):
    """attempts to convert all kinds of unicode txt with e.g. tex or html accents to plain unicode suitable for utf-8 encoding of all accents"""
    ## first convert html accents
    txt = hparser.unescape(txt)
    ## next convert tex accents
    txt = tex2utf8(txt)
    return txt

def txt2ascii(txt):
    """composition of txt2utf8() and uni2ascii """
    txt = txt2utf8(txt)
    txt = uni2ascii(txt)
    return txt



if __name__ == '__main__':
    #d = make_utf8_to_tex()
    #print d
    #print e
    tex = '\\\'Ecole Normale Sup\\\'erieur'
    tex = '$\\\'Ecole Normale Sup\\\'erieur$\\\'Ecole Normale Sup\\\'erieur$\'e\'e$'

    #tex = 'Jan Ob\\l\\\'oj'
    #tex = '\\\'o'
    tex = 'D\\\'{e}composition des tribus $F_{(T+t)+}^{0}$  d\'un processus continu \\`a droite'
    print tex
    print tex2utf8(tex)
    #print convert(tex,tex2utf8).encode('utf-8')
    #print apply_outside_dollars(tex,tex2utf8).encode('utf-8')
    #tex = '\\\'e'
    #print tex
    #print convert(tex,tex2utf8).encode('utf-8')
    
    #for k,v in tex2utf8.items():
    #    print k,v


