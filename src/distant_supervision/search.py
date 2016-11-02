import pickle
import uuid

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
        if query not in self.search_log:
            search_uuid = uuid.uuid1()
            search_strategy(search_uuid,query)
            self.search_log[query] = str(search_uuid)
            entry = (query,str(search_uuid))
            pickle.dump(entry, open("data/distant_supervision/queries.p", "ab+"))

        filename = "data/distant_supervision/raw_queries/" + self.search_log[query]




    def instance():
        if Search.s is None:
            Search.s = Search()

        return Search.s

    instance = staticmethod(instance)






if __name__ == "__main__":
    Search.instance().search("test")

    Search.instance().search("america")

    Search.instance().search("test")
