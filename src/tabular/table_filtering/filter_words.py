from distant_supervision.query_generation import normalise_keep_nos
from tabular.table_collection import TableCollection
from tabular.table_filtering.filter import Filter


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

