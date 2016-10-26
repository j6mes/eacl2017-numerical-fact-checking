import csv
import random
import itertools
import string

from util import *

from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics.pairwise import cosine_similarity

from feature_eng import *


import numpy as np

class TableQuestionAnswerTuple:

    exclude = set(string.punctuation)

    def __init__(self,id,question,table,answer):
        self.id = id
        self.question = (''.join(ch for ch in question if ch not in self.exclude))
        self.table_path = table
        self.answer = answer


    def read_table(self):
        rows = []
        header = []

        header_read = False
        with open("WikiTableQuestions/"+self.table_path.replace(".csv",".tsv")) as table:
            #check if header
            has_header = csv.Sniffer().has_header(table.readline())
            table.seek(0)

            for line in csv.reader(table, delimiter="\t"):
                if(has_header and not header_read):
                    header = line
                    header_read = True
                else:
                    rows.append(line)
        return (header,rows)

    def load(self):
        tab = self.read_table()
        self.header = tab[0]
        self.rows = tab[1]

    def generateFeaturesForCorrect(self):
        return self.features(self.header),1

    def generateFeaturesForIncorrect(self,objs):
        obj = random.choice(objs)
        while(obj.id is  self.id):
            obj = random.choice(objs)

        return [(self.features(obj.header),0)]

    def genAll(self,objs):
        ret = []
        for obj in objs:
            if obj.id is self.id:
                continue
            ret.append((self.features(obj.header),0))

        return ret

    def features(self,header):
        h = []
        h.extend(j.lower().split(" ") for j in header)
        h=[''.join(ch for ch in a if ch not in self.exclude) for a in list(itertools.chain.from_iterable(h))]

        words = (''.join(ch for ch in self.question if ch not in self.exclude)).split(" ")
        w = bow(words,h)


        allngrams_words = []
        for word in words:
            allngrams_words.extend(character_ngram(word))

        allngrams_header = []
        for word in h:
            allngrams_header.extend(character_ngram(word))

        cw = bow(allngrams_words,allngrams_header)

        headerwords = set()
        for word in self.header:
            headerwords.update(normalise(word).split())

        questionwords = set(normalise(self.question).split())

        ret = [1,
                cosine_similarity([w[0]],[w[1]])[0][0],
                jaccard_similarity_score([1 if a > 0 else 0 for a in w[0]],
                                         [1 if a > 0 else 0 for a in w[1]]),

                cosine_similarity([cw[0]],[cw[1]])[0][0],
                jaccard_similarity_score([1 if a > 0 else 0 for a in cw[0]],
                                         [1 if a > 0 else 0 for a in cw[1]]),


                ]

        #intersection of BOWs
        if(experiment == 1 or experiment == 3):
            ret.extend(np.maximum(global_bow(vocab,headerwords),global_bow(vocab,questionwords)))

        #union of BOWs
        if(experiment == 2 or experiment == 3):
            ret.extend(np.minimum(global_bow(vocab, headerwords), global_bow(vocab, questionwords)))

        return ret