from collections import defaultdict

from distant_supervision.query_generation import normalise, normalise_keep_nos
from tabular.table_collection import TableCollection
from tabular.table_reader import read_table, number_entity_tuples, table_nes
from wikitablequestions.dataset_reader import load_instances


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





class AllWordsFiltering(Filter):
    def register(self,file):
        table = TableCollection.instance().load(file)

        for row in table['rows']:
            for col in row:
                self.register_word(col, file)


    def register_word(self,word,table):
        self.words_to_table_exact[normalise_keep_nos(word)].add(table)

        for w in word.split():
            self.words_to_table_partial[normalise_keep_nos(w)].add(table)



class FilterTableNEs(Filter):
    def register(self,file):
        table = TableCollection.instance().load(file)
        nes = table_nes(table)

        for ne in nes:
            if len(normalise_keep_nos(ne)) > 0:
                self.words_to_table_exact[normalise_keep_nos(ne)].add(file)

                for word in normalise_keep_nos(ne).split(" "):
                    if len(word) >0:
                        self.words_to_table_exact[word].add(file)



def load_collection(name, filtering_strategy=AllWordsFiltering):
    instances = load_instances(name)
    filtering = filtering_strategy()

    for instance in instances:
        filtering.register(instance['table'])

    return filtering


def write_collection(name,tables,base="data/WikiTableQuestions/data/"):
    with open(base+name+".tsv","w+") as f:
        f.write("id\tutterance\ttable\tvalue\n")
        id = 0

        for table in tables:
            f.write("f-"+str(id)+"\tNone\t"+table+"\tNone\n")
            id += 1



if __name__ == "__main__":
    instances = load_instances("herox")
    filtering = FilterTableNEs()

    for instance in instances:
        file = instance['table']
        filtering.register(file)

    print(filtering.words_to_table_exact)
    print(filtering.words_to_table_exact)

