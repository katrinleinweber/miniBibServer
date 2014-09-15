# from hammock import Hammock as Github
import json
import urllib
import datetime
import sys
import base64
from pprint import pprint
from bs4 import BeautifulSoup

from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding("utf-8")

html = urllib.urlopen('http://theguardian.co.uk')
soup = BeautifulSoup(html)

spans = soup.find_all('div', attrs={'class':'trail-text'})

con = u""
for item in spans:
    if item.string:
        yay = item.string.strip()
        yay = ' '.join([word for word in yay.split() if word not in (stopwords.words('english'))])
        con += yay.encode("utf-8") + u"\n"
print con
