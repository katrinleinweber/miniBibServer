from os import listdir
from os.path import isfile, join
import ims_legacy

onlyfiles = [ f for f in listdir('texfiles') if isfile(join('texfiles',f)) ]

def make_all():
    for f in onlyfiles:
        base = unicode(f.split('.tex',1)[0],'utf-8')
        print "making new html file: " + base + ".html"
        html = ims_legacy.make_one(join('texfiles',f))
        o = open("./htmlfiles/" + base + '.html', 'w')
        o.write(html.encode('utf-8'))
        o.close()

def make_one(filename):
    html = ims_legacy.make_one(join('texfiles',filename))
    base = unicode(filename.split('.tex',1)[0],'utf-8')
    o = open("./htmlfiles/" + base + '.html', 'w')
    o.write(html.encode('utf-8'))
    o.close()
    print "made new html file: " + base + ".html"
