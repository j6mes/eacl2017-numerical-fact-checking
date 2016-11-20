from collections import defaultdict

from distant_supervision.query_generation import normalise
from tabular.table_collection import TableCollection
from tabular.table_reader import read_table
from wikitablequestions.dataset_reader import load_instances

class Filtering():
    def __init__(self):
        self.words_to_table_exact = defaultdict(set)
        self.words_to_table_partial = defaultdict(set)

    def register_word(self,word,table):
        self.words_to_table_exact[normalise(word)].add(table)

        for w in word.split():
            self.words_to_table_partial[normalise(w)].add(table)

    def get_tables_for_word(self,word):
        return {"exact":self.words_to_table_exact[normalise(word)],
            "partial": [self.words_to_table_partial[normalise(w)] for w in word.split()]}

def filter():
    pass

if __name__ == "__main__":
    instances = load_instances("training")


    filtering = Filtering()

    for instance in instances:
        table = TableCollection.instance().load(instance['table'])

        for row in table['rows']:
            for col in row:
                filtering.register_word(col,instance['table'])


    print(filtering.get_tables_for_word("1st"))
    print(filtering.get_tables_for_word("Quarterfinals"))
