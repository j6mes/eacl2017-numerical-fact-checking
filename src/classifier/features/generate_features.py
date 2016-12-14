import os
import pickle
import re
from collections import defaultdict
import numpy as np
from sklearn.linear_model import LogisticRegression

from classifier.Classifier import Classifier
from classifier.features.bow import BOW
from classifier.features.linearise import flatten_without_labels
from classifier.features.pseudo_multiclass import IDPerColumnMultiClass
from distant_supervision.clean_html import has_text
from distant_supervision.normalisation import normalise_keep_nos
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.synonyms import SynonymRegistry
from factchecking.question import Question
from tabular.tuples import get_all_tuples


def num(s):
    s = re.sub(r"[^0-9\.]+", "", s.replace(",", ""))
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None

def is_num(s):
    return num(s) is not None

def hmi(sentence, sentence1):
    return 1 if len(
        set(normalise_keep_nos(sentence).split()).intersection(set(normalise_keep_nos(sentence1).split()))) > 0 else 0


def get_synonyms(word):
    return SynonymRegistry.instance().get(word)



class FeatureGenerator():
    def generate_training(self, world = "herox"):
        base = "data/distant_supervision/features/"

        if not os.path.exists(base):
            print("creating dir " + base)
            os.makedirs(base)

        found_features = []
        with open("data/distant_supervision/queries_" + world + ".txt", "r") as file:
            lines = file.readlines()
            num_qs = len(lines)
            done = 0

            for line in lines:
                print("Done: " + str(done * 100 / num_qs))

                done += 1
                query = line.replace("\n", " ").strip().split("\t")

                table = query[0]
                targets = query[1].strip().replace(",", "").split("-")
                search = query[2]

                if search.split("\" \"")[1].replace("\"", "").isnumeric():
                    print("skipped")
                    print(query)
                else:
                    for target in targets:
                        entity = query[2].split("\" \"")[0][1:]
                        relation = query[2].split("\" \"")[1][:-1]

                        urls = Search.instance().search(search)

                        for url in urls:
                            filename = url_hash(url + "__" + search + "__" + target + "__" + table) + ".p"

                            if has_text(url) and os.path.exists(base + filename):
                                with open(base + filename, 'rb') as f:
                                    features = pickle.load(f)

                                    for feature in features:
                                        feature['table'] = table
                                        feature['relation'] = relation

                                    found_features.extend(features)
                            else:
                                pass

        print("Registering words in BOW")
        n_feats = len(found_features)
        done = 0

        self.bow = BOW()
        for feature in found_features:
            words = (flatten_without_labels({"bow": feature['complete_bow']}))

            for word in words:
                self.bow.register(word)
            done += 1

            if done % 5000 == 0:
                print(str(done * 100 / n_feats) + "%")



        print("Registering columns")
        self.mc = IDPerColumnMultiClass()
        for feature in found_features:
            self.mc.register(feature['table'], feature['relation'])

        Xs = []
        ys = []

        print("Counting features")
        total_pos = 0
        total_neg = 0
        for feature in found_features:
            if feature['class'] == 0:
                total_neg += 1
            else:
                total_pos += 1

        print("Total positive: " + str(total_pos))
        print("Total negative: " + str(total_neg))

        print("Looking for positive features")

        done = 0
        num_correct = defaultdict(int)
        for feature in found_features:
            y = feature['class']

            if y == 1:
                num_correct[feature['relation']] += 1

                if done % 100 == 0:
                    print(done)
                done += 1

                words = (flatten_without_labels({"bow": feature['complete_bow']}))
                X = np.hstack((1, self.mc.get(feature['table'], feature['relation']), feature['header_match_intersection'],
                               self.bow.convert_one_hot(words)))

                Xs.append(X)
                ys.append(y)



        print("Subsampling negative features")
        done = 0
        num_incorrect = defaultdict(int)
        for feature in found_features:
            y = feature['class']

            if y == 0 and num_incorrect[feature['relation']] < num_correct[feature['relation']]:
                if done % 100 == 0:
                    print(done)

                done += 1

                num_incorrect[feature['relation']] += 1
                words = (flatten_without_labels({"bow": feature['complete_bow']}))
                X = np.hstack((1, self.mc.get(feature['table'], feature['relation']), feature['header_match_intersection'],
                               self.bow.convert_one_hot(words)))

                Xs.append(X)
                ys.append(y)

        return Xs, ys
        # pickle.dump(Xs, open("dump.x","w+"))
        # pickle.dump(ys, open("dump.y","w+"))
        # pickle.dump(bow.words,open("dump.bow","w+"))
        # pickle.dump(mc.headers.words,open("dump.mc","w+"))

    def generate_test(self, tables, question):
        q = question
        q.parse()

        tuples = []
        for obj in q.nps.union(q.nes):
            tuples.extend(get_all_tuples(tables, obj))
            for synonym in get_synonyms(obj):
                tuples.extend(get_all_tuples(tables, synonym))


        Xs = []

        for tuple in tuples:
            table_name = tuple[0]
            rel_name = tuple[1]['relation']
            words = normalise_keep_nos(question.text).split()

            q_bow = flatten_without_labels({"bow": self.bow})

            X = np.hstack((1, self.mc.get(table_name, rel_name), hmi(question.text, rel_name), self.bow.convert_one_hot(q_bow)))
            Xs.append(X)

        return tuples,Xs


