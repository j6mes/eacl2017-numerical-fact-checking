import os
import pickle

from distant_supervision.normalisation import normalise_keep_nos
from tabular.table_collection import TableCollection
from tabular.table_filtering.filter import Filter
from tabular.table_filtering.filter_nes import FilterTableNEs
from tabular.table_reader import table_nes


class FilterTableNEsMemoized(FilterTableNEs):

    def __init__(self,world,base="data/distant_supervision/"):
        super().__init__()
        self.base = base
        self.files = set()
        self.world = world
        if os.path.exists(base+"filters"+world+".p"):
            with open(base+"filters"+world+".p","rb") as file:
                data = pickle.load(file)
                self.words_to_table_partial = data['partial']
                self.words_to_table_exact = data['exact']

                self.files = data['files']

    def register(self,file):
        world = self.world
        print("register table "+ file)
        if file not in self.files:
            print("loading from file")
            super().register(file)
            self.files.add(file)
            with open(self.base+"filters"+world+".p","wb+") as f:
                data = dict()
                data['partial'] = self.words_to_table_partial
                data['exact'] = self.words_to_table_exact
                data['files'] = self.files

                pickle.dump(data,f)
