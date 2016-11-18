import sys

from distant_supervision.clean_html import get_text
from distant_supervision.search import Search


if __name__ == "__main__":
    world = sys.argv[1]

    with open("data/distant_supervision/queries_"+world+".txt", "r") as file:
        lines = file.readlines()
        num_qs = len(lines)
        done = 0
        for line in lines:
            done += 1
            query = line.replace("\n"," ").strip().split("\t")

            table = query[0]
            search = query[2]


            if search.split("\" \"")[1].replace("\"","").isnumeric():
                print("skipped")
                print (query)
            else:
                urls = Search.instance().search(search)

                for url in urls:
                    print(url)
                    print(get_text(url))

                print(str(100*done/num_qs) + "%")