import os
import hashlib

import urllib3


def get_page_contents(url):

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36"}
    http = urllib3.PoolManager()

    try:
        r = http.request('GET', url,headers=headers,timeout=5.0)
    except:
        return "".encode()
    print("Got data")

    content_type = r.headers['Content-Type']
    if "html" in content_type.lower():
        return r.data

    return b""

def url_hash(url):
    return hashlib.sha256(str.encode(url)).hexdigest()


def get_path():
    return "data/distant_supervision/scraped_pages"

def save_page_disk(url):

    hash = url_hash(url)

    pathName = get_path()

    if not os.path.exists(pathName):
        print("creating dir " + pathName)
        os.makedirs(pathName)

    data = get_page_contents(url)


    with open(pathName+"/"+hash+".html","wb+") as file:
        file.write(data)

def get_page(url):
    path = get_path() + "/" + url_hash(url) + ".html"
    if not os.path.exists(path):
        save_page_disk(url)

    with open(path,'rb') as file:
        return "\n".join([bytes.decode(line.strip(),errors="replace") for line in file.readlines()])





if __name__ == "__main__":
    save_page_disk("http://bbc.co.uk")
    print(get_page("http://bbc.co.uk"))