# -*- coding: utf-8 -*-
import os
import re

from bs4 import BeautifulSoup

from distant_supervision.scraper import get_page_contents, url_hash, get_page


def clean_html(html):
    replaceBrs = re.compile(r"<br */? *>[ \r\n]*<br */? *>")

    html = re.sub(r'<style.*>.*</style>',r"",html)
    html = re.sub(r'<script.*>.*</script>', r"", html)
    html = re.sub(r'<div class="[^"]*?paragraph[^"]*?">(.*?)</div>', r"<p>\1</p>", html)
    html = re.sub(r"<div class='[^']*?paragraph[^']*?'>(.*?)</div>", r"<p>\1</p>", html)
    html = re.sub(r'<div class="[^"]*?para[^"]*?">(.*?)</div>', r"<p>\1</p>", html)
    html = re.sub(r"<div class='[^']*?para[^']*?'>(.*?)</div>", r"<p>\1</p>", html)

    html = re.sub(replaceBrs, "</p><p>", html)

    return html

def haschild(elem):
    for child in elem:
        if child.name == "p" or child.name=="div" or child.name=="article":
            return True
    return False


def text_from_html(tag,original_html):
    soup = BeautifulSoup(original_html,"lxml")

    if soup.find('body') is not None:
        paras = soup.find('body').find_all(['p','div','article'])
    else:
        return ""

    counts = dict()
    pobjs = dict()

    for p in paras:
        if not haschild(p.contents) and len(p.getText().split(" ")) > 10:

            if len(p.select("a")) > 0:
                text = p.__str__()

                for repl in p.select("a"):
                    text = text.replace(repl.__str__(),"")

                i = BeautifulSoup(text,"lxml").getText().strip()
                if len(i) > 5 and len(i.split(" ")) > 5:
                    continue


            parent = p.parent().__str__()
            if parent in counts:
                counts[parent] += 1
            else:
                counts[parent] = 1
                pobjs[parent] = p.parent()



    maxp = 0
    topparent = None
    for p in counts.keys():
        if counts[p] > maxp:
            maxp = counts[p]
            topparent = pobjs[p]


    out = []
    if topparent is not None:

        for i in topparent:
            if i.name == tag:
                if len(i.select("a")) > 0:
                    text = i.__str__()

                    for repl in i.select("a"):
                        text = text.replace(repl.__str__(),"")

                    if len(i.getText()) > 5 and len(BeautifulSoup(text,"lxml").getText().strip()) is not 0 and len(BeautifulSoup(text,"lxml").getText().split(" ")) > 5:
                        out.append(i.getText().strip())
                elif len(i.getText()) > 5 and len(i.getText().split(" ")) > 5:
                    out.append(i.getText().strip())

    return "\n".join(line for line in ("\n".join(out)).split("\n") if len(line.strip())>5)


def get_text_path():
    return "data/distant_supervision/scraped_texts"


def save_text_disk(url):
    hash = url_hash(url)

    pathName = get_text_path()

    if not os.path.exists(pathName):
        print("creating dir " + pathName)
        os.makedirs(pathName)

    data = get_page(url)
    data = text_from_html("p",clean_html(data))

    with open(pathName+"/"+hash+".txt","w+") as file:
        file.write(data)


def has_text(url):
    path = get_text_path() + "/" + url_hash(url) + ".txt"
    return os.path.exists(path)


def get_text(url):
    path = get_text_path() + "/" + url_hash(url) + ".txt"
    if not os.path.exists(path):
        save_text_disk(url)

    with open(path, 'r') as file:
        data = file.read()
        if "<script" in data.lower():
            return ""
        return data



if __name__ == "__main__":
    #print(text_from_html("p",clean_html(bytes.decode(get_page_contents("http://www.bbc.co.uk/news/election-us-2016-37854525")))))
    #print(text_from_html("p",clean_html(bytes.decode(get_page_contents("https://en.wikipedia.org/wiki/United_States")))))
    #print(text_from_html("p",clean_html(bytes.decode(get_page_contents("https://en.wikipedia.org/wiki/Linear_cryptanalysis")))))

    print(get_text("http://www.bbc.co.uk/news/election-us-2016-37854525"))
