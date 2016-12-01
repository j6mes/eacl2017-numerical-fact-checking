from _license import defaultdict

from distant_supervision.query_generation import normalise_keep_nos


class Filter():
    def __init__(self):
        self.words_to_table_exact = defaultdict(set)
        self.words_to_table_partial = defaultdict(set)


    def register(self,file):
        pass


    def get_tables(self,word):
        r = [self.words_to_table_partial[normalise_keep_nos(w)] for w in word.split()]

        partial = set()
        for result in r:
            partial.update(result)

        return {"exact":self.words_to_table_exact[normalise_keep_nos(word)],
            "partial": partial}


