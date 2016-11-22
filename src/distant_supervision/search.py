import json
import os
import pickle
import uuid

from distant_supervision.query_generation import normalisequery
from distant_supervision.strategy.bing import bing_query

class Search:
    s = None

    def __init__(self):
        self.search_log = dict()

        try:
            with open("data/distant_supervision/queries.p","rb") as f:
               while 1:
                    try:
                        entry = pickle.load(f)
                        self.search_log[entry[0]] = entry[1]
                    except EOFError:
                        break
        except:
            pass


    def search(self,query,search_strategy=bing_query):
        print("Search for "+ query)
        if normalisequery(query) not in self.search_log:
            print("New Query")
            search_uuid = uuid.uuid1()
            search_strategy(search_uuid,query)
            self.search_log[normalisequery(query)] = str(search_uuid)
            entry = (normalisequery(query),str(search_uuid))
            pickle.dump(entry, open("data/distant_supervision/queries.p", "ab+"))

        else:
            print("Query already executed")


        filename = "data/distant_supervision/raw_queries/" + self.search_log[normalisequery(query)] + ".json"

        urls = []
        if os.path.exists(filename):
            with open(filename,'r') as f:
                contents = json.load(f)
                for link in contents:
                    urls.append(link['displayUrl'])
        else:
            for item in self.search_log.keys():
                if self.search_log[item] == self.search_log[normalisequery(query)]:
                    continue

                pickle.dump((item,self.search_log[item]), open("data/distant_supervision/new_queries.p", "ab+"))

            print("Missing file. Remove from dictionary and search again")
            self.search_log.pop(normalisequery(query), None)
            os.rename("data/distant_supervision/new_queries.p","data/distant_supervision/queries.p")

            return self.search(query)



        return urls


    def instance():
        if Search.s is None:
            Search.s = Search()

        return Search.s

    instance = staticmethod(instance)






if __name__ == "__main__":
    print(Search.instance().search("america"))
