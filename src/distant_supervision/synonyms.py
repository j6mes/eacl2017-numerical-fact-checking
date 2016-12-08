import os
from collections import defaultdict
import pickle

from distant_supervision.query_generation import normalise


class SynonymRegistry():
    def __init__(self):
        self.synonyms = defaultdict()
        self.synonyms.setdefault(list)
        self.load()

    def load(self,base="data/distant_supervision/"):
        if os.path.exists(base+"syn.p"):
            self.synonyms = pickle.load(open(base+"syn.p","r+"))
        else:
            self.seed()

    def get(self,word):
        if normalise(word) in self.synonyms:
            return self.synonyms[normalise(word)]
        return []

    def seed(self):
        self.synonyms["usa"] = ["united states","america","us"]
        self.synonyms["america"] = ["united states", "usa","us"]
        self.synonyms["doctor"] = ["doctors", "physicians","physician"]
        self.synonyms["doctors"] = ["doctor", "physicians", "physician"]
        self.synonyms["doctors"] = ["doctor", "physicians", "physician"]
        self.synonyms["physicians"] = ["doctor", "doctors", "physician"]
        self.synonyms["physician"] = ["doctor", "doctors", "physicians"]

    tc = None
    def instance():
        if SynonymRegistry.tc is None:
            SynonymRegistry.tc = SynonymRegistry()
        return SynonymRegistry.tc

    instance = staticmethod(instance)

