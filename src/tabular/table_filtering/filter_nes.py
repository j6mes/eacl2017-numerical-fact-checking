from distant_supervision.normalisation import normalise_keep_nos
from distant_supervision.stop_words import StopWords
from tabular.table_collection import TableCollection
from tabular.table_filtering.filter import Filter
from tabular.table_reader import table_nes


class FilterTableNEs(Filter):
    def register(self,file):
        table = TableCollection.instance().load(file)
        nes = table_nes(table)

        for ne in nes:
            nen = normalise_keep_nos(ne).strip()

            if len(nen) > 0:
                self.words_to_table_exact[nen].add(file)

                for word in nen.split(" "):
                    if word not in StopWords.instance().words:
                        self.words_to_table_partial[word].add(file)
