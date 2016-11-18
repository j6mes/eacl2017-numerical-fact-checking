import sys

from distant_supervision.search import Search


if __name__ == "__main__":
    world = sys.argv[1]

    with open("data/distant_supervision/queries_"+world+".txt", "r") as file:
        for line in file:
            query = line.replace("\n"," ").strip().split("\t")

            table = query[0]
            search = query[1]

            if search.split("\" \"")[2].replace("\"","").isnumeric():
                print("skipped")
                print (query)
            else:
                Search.instance().search(search)