# -*- encoding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib3
import xml.etree.ElementTree as ET
import sqlite3
import os.path
import re

datebase_name = "dominion.db"


def scraping(url, filename, encoding_flag):
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', url)
        if encoding_flag is True:
            soup = BeautifulSoup(response.data.decode('shift_jis'))
            html = '<root>'+str(soup)+'</root>'
        else:
            soup = BeautifulSoup(response.data)
            html = str(soup)
        #soup = response.data.decode('shift_jis')
        with open(filename, "w") as f:
            f.write(str(html))
    except:
        print("htmlを取得できませんでした")


def parse_to_db1(html):
    tree = ET.parse(html)
    keys = []
    try:
        dominion = sqlite3.connect(datebase_name)
    except:
        print("データベースに接続できません")
        exit()
    cur = dominion.cursor()
    sql = "delete from cards;"
    cur.execute(sql)
    for record in tree.findall(".//tr[@class]"):
        for key in record.findall('.//td'):
            if key.text is None:
                name = key.find("a")
                keys.append(name.text)
                continue
            text = key.text
            text = text.replace("\'", "\'\'")
            if text == '-':
                text = 0
            if text == '▲1':
                text = -1
            keys.append(text)
        print(keys)
        if keys[0].isdigit() is not True:
            keys = []
            continue
        sql = "insert into cards values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', %d, %d, %d, %d, %d)" % (int(keys[0]), keys[1], keys[2], keys[3], keys[4], keys[5], keys[6], keys[7], keys[8], int(keys[9]), keys[10], int(keys[11]), int(keys[12]), int(keys[13]), int(keys[14]), int(keys[15]))
        cur.execute(sql)
        print(sql)
        dominion.commit()
        keys = []
    cur.close()


def parse_to_db2(html):
    tree = ET.parse(html)
    keys = []
    i = 0
    pattern = re.compile('(.+)(/)')
    try:
        dominion = sqlite3.connect(datebase_name)
    except:
        print("データベースに接続できません")
        exit()
    cur = dominion.cursor()
    sql = "delete from touhou;"
    cur.execute(sql)
    for record in tree.findall(".//tr[@dir='ltr']"):
        if i < 2:
            i += 1
            keys = []
            continue
        for key in record.findall('.//td'):
            text = key.text
            if text is not None:
                text = text.replace("\'", "\'\'")
            keys.append(text)
        if keys[1].isdigit() is not True:
            keys = []
            continue

        result = pattern.search(keys[3])
        keys[3] = result.group(1)
        print(keys)

        sql = "insert into touhou values(%d, '%s', '%s', '%s');" % (i-2, keys[3], keys[16], keys[17])
        cur.execute(sql)
        dominion.commit()
        keys = []
        i += 1
    cur.close()


def db_create():
    dominion = sqlite3.connect(datebase_name)
    sql = """
    create table cards(
        id interger,
        name varchar,
        pronunciation varchar,
        eng_name varchar,
        setname varchar,
        cost varchar,
        portion varchar,
        attr varchar,
        kind varchar,
        zaihou integer,
        victory varchar,
        card integer,
        action integer,
        buy integer,
        coin integer,
        victory_token integer);
    """
    dominion.execute(sql)
    sql2 = """
    create table touhou(
        id integer,
        name varchar,
        koumakyou varchar,
        youyoumu varchar);
    """
    dominion.execute(sql2)
    dominion.close()


def main():
    url1 = "http://suka.s5.xrea.com/dom/list.cgi"
    url2 = "https://docs.google.com/spreadsheet/pub?key=0AtJL7cj3CdLfdFY1cGZrQldaUFdER1VoZUJLam9Rc2c&chrome=false&gid=0"
    if not os.path.exists(datebase_name):
        db_create()
    scraping(url1, "dominion1.html", True)
    parse_to_db1("dominion1.html")
    scraping(url2, "dominion2.html", False)
    parse_to_db2("dominion2.html")

if __name__ == "__main__":
    main()
