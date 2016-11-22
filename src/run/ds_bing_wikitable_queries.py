import sys

from distant_supervision.search import Search


if __name__ == "__main__":
    world = sys.argv[1]

    with open("data/distant_supervision/queries_"+world+".txt", "r") as file:
        for line in file:
            query = line.replace("\n"," ").strip().split("\t")

            print(query)
            table = query[0]
            search = query[2]

            if search.split("\" \"")[1].replace("\"","").isnumeric():
                print("skipped")
                print (query)
            else:
                Search.instance().search(search)