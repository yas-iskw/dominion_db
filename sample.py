# -*- encoding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib3
import xml.etree.ElementTree as ET
import sqlite3


#def scraping(url):
#   response = urllib2.urlopen(url)
#    soup = BeautifulSoup(response.read(), fromEncoding='utf-8')
#    with open("dominion.html", "w") as f:
#        f.write(str(soup))


def parse_to_db(html):
    i = 0
    tree = ET.parse(html)
    keys = []
    for record in tree.findall(".//tr[@dir='ltr']"):
        #print(record.text)
        for key in record.findall('.//td'):
            keys.append(key.text)
        print(keys)
        keys = []
    #print i


def main():
    #url = "https://docs.google.com/spreadsheet/pub?key=0AtJL7cj3CdLfdFY1cGZrQldaUFdER1VoZUJLam9Rc2c&chrome=false&gid=0"
    #scraping(url)
    parse_to_db("dominion2.html")

if __name__ == '__main__':
    main()