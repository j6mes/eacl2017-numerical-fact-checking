import re

from bs4 import BeautifulSoup

from distant_supervision.scraper import get_page_contents


def clean_html(html):
    replaceBrs = re.compile(r"<br */? *>[ \r\n]*<br */? *>")

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


def getcontent(tag,original_html):
    soup = BeautifulSoup(original_html,"lxml")

    paras = soup.find('body').find_all(['p','div','article'])

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

                    print (i.getText())
                    if len(i.getText()) > 5 and len(BeautifulSoup(text,"lxml").getText().strip()) is not 0 and len(BeautifulSoup(text,"lxml").getText().split(" ")) > 5:
                        out.append(i.getText().strip())
                elif len(i.getText()) > 5 and len(i.getText().split(" ")) > 5:
                    out.append(i.getText().strip())

    return "\n".join(line for line in ("\n".join(out)).split("\n") if len(line.strip())>5)




if __name__ == "__main__":
    print(getcontent("p",clean_html(bytes.decode(get_page_contents("http://www.bbc.co.uk/news/election-us-2016-37854525")))))


    print(getcontent("p",clean_html(bytes.decode(get_page_contents("https://en.wikipedia.org/wiki/United_States")))))

    print(getcontent("p",clean_html(bytes.decode(get_page_contents("https://en.wikipedia.org/wiki/Linear_cryptanalysis")))))
