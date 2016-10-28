import csv
import random
import itertools
import string

import sys

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

    def load_global(self):
        questionwords = set(normalise(self.question).split())
        self.qbow = global_bow(vocab,questionwords)
        self.qngs = global_bow(vocab_ngrams, character_ngram_nw(normalise(self.question)))

        headerwords = set()
        for word in self.header:
            headerwords.update(normalise(word).split())

        self.hngs = global_bow(vocab_ngrams, character_ngram_nw(normalise(" ".join(self.header))))
        self.hbow = global_bow(vocab, normalise(" ".join(headerwords)))

    def gen_q_features(self):
        questionwords = set(normalise(self.question).split())
        self.qbow = global_bow(vocab, questionwords)
        self.qngs = global_bow(vocab_ngrams, character_ngram_nw(normalise(self.question)))

    def generateFeaturesForCorrect(self):
        return self.features(self.header,self.hbow,self.hngs),1

    def generateFeaturesForIncorrect(self,objs):
        obj = random.choice(objs)
        # AV: replaced "is" with "==": see here for explanation
        # http://stackoverflow.com/questions/22885931/when-if-ever-to-use-the-is-keyword-in-python
        while(obj.id == self.id):
            obj = random.choice(objs)

        return [(self.features(obj.header,obj.hbow,obj.hngs),0)]

    def genAll(self,objs):
        ret = []
        for obj in objs:
            # AV: removed this so that it generates features for all tables including the correct one.
            #if obj.id == self.id:
            #    continue
            # AV: Changed this from assuming all incorrect (0) to None
            # AV: also made it return the table id itself
            ret.append((self.features(obj.header,obj.hbow,obj.hngs), 1 if obj.id == self.id else 0, obj.table_path))

        return ret

    def features(self,header,hbow,hng):
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



        ret = [1,
                cosine_similarity([w[0]],[w[1]])[0][0],
                jaccard_similarity_score([1 if a > 0 else 0 for a in w[0]],
                                         [1 if a > 0 else 0 for a in w[1]]),

                cosine_similarity([cw[0]],[cw[1]])[0][0],
                jaccard_similarity_score([1 if a > 0 else 0 for a in cw[0]],
                                         [1 if a > 0 else 0 for a in cw[1]]),


                ]






        experiment_bow = int(sys.argv[1])
        #intersection of BOWs
        if(experiment_bow == 1 or experiment_bow == 3):
            ret.extend(np.maximum(hbow,self.qbow))

        #union of BOWs
        if(experiment_bow == 2 or experiment_bow == 3):
            ret.extend(np.minimum(hbow, self.qbow))



        experiment_ngrams = int(sys.argv[2])
        #intersection of ngrams
        if(experiment_ngrams == 1 or experiment_ngrams == 3):
            ret.extend(np.maximum(hng,self.qngs))

        #union of ngrams
        if(experiment_ngrams == 2 or experiment_ngrams == 3):
            ret.extend(np.minimum(hng, self.qngs))

        return ret
