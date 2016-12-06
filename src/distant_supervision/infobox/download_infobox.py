from distant_supervision.scraper import raw_req
import json

def download_infobox(query,base="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&rvsection=0&titles="):
    data = json.loads(raw_req(base+query).data.decode())
    pages = data['query']['pages']
    for key in pages.keys():
        ft =pages[key]['revisions'][0]['*']
        lines = ft.split("\n")
        for line in lines:
            if len(line)>0 and line[0]=="|":
                key = line[1:].split(" =")[0].strip()
                value = line[1:].split(" =")[1].strip()
                if len(value) == 0:
                    value = lines[lines.index(line)+1]
                print((key,value))


if __name__=="__main__":
    download_infobox("Hamas")
    download_infobox("The_Walt_Disney_Company")