import os
import pickle
import re
import sys

from sklearn.linear_model import LogisticRegression

from classifier.features.bow import BOW
from classifier.features.linearise import flatten_with_labels, flatten_without_labels
from classifier.features.pseudo_multiclass import IDPerColumnMultiClass
from distant_supervision.clean_html import get_text, has_text
from distant_supervision.query_generation import normalise
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.utterance_detection import find_utterances_for_tuple, matches_to_features, threshold_match

import numpy as np

from factchecking.question import Question
from tabular.filtering import load_collection
from tabular.tuples import get_all_tuples


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def hmi(sentence, sentence1):
    print(len(set(normalise(sentence).split()).intersection(set(normalise(sentence1).split()))))
    return 1 if len(
        set(normalise(sentence).split()).intersection(set(normalise(sentence1).split()))) > 0 else 0

if __name__ == "__main__":
    world = sys.argv[1]
    base = "data/distant_supervision/features/"

    if not os.path.exists(base):
        print("creating dir " + base)
        os.makedirs(base)

    found_features = []
    with open("data/distant_supervision/queries_"+world+".txt", "r") as file:
        lines = file.readlines()
        num_qs = len(lines)
        done = 0
        for line in lines:
            done += 1
            query = line.replace("\n"," ").strip().split("\t")

            table = query[0]
            target = query[1]
            search = query[2]

            if search.split("\" \"")[1].replace("\"","").isnumeric():
                print("skipped")
                print (query)
            else:

                entity = query[2].split("\" \"")[0][1:]
                relation = query[2].split("\" \"")[1][:-1]

                urls = Search.instance().search(search)

                for url in urls:
                    print(url)
                    print(url_hash(url))
                    filename = url_hash(url + "__"+ search + "__" + target + "__" + table) + ".p"
                    print(filename)
                    print(has_text(url))
                    print(os.path.exists(base+filename))
                    if has_text(url) and os.path.exists(base+filename):

                        with open(base+filename, 'rb') as f:
                            features = pickle.load(f)

                            for feature in features:
                                feature['table'] = table
                                feature['relation'] = relation


                            print("found ")
                            found_features.extend(features)
                    else:
                        pass





    bow = BOW()
    for feature in found_features:
        words = (flatten_without_labels({"bow":feature['complete_bow']}))
        for word in words:
            bow.register(word)


    mc = IDPerColumnMultiClass()
    for feature in found_features:
        mc.register(feature['table'],feature['relation'])


    Xs = []
    ys = []

    num_correct = 0
    for feature in found_features:
        y = feature['class']

        if y == 1:
            num_correct += 1
            words = (flatten_without_labels({"bow": feature['complete_bow']}))
            X = np.hstack((1, mc.get(feature['table'],feature['relation']), feature['header_match_intersection'], bow.convert_one_hot(words)))

            print(X)
            Xs.append(X)
            ys.append(y)


    num_incorrect = 0
    for feature in found_features:
        y = feature['class']

        if y == 0 and num_incorrect < 2*num_correct:
            num_incorrect += 1
            words = (flatten_without_labels({"bow": feature['complete_bow']}))
            X = np.hstack((1, mc.get(feature['table'],feature['relation']), feature['header_match_intersection'], bow.convert_one_hot(words)))

            print(X)
            Xs.append(X)
            ys.append(y)

    lr = LogisticRegression()
    lr.fit(Xs,ys)

    queries = ["Exxon Mobil reached a total value of $772 million in 2007.",
               "Around 90,000 unaccompanied children claimed asylum in the EU in 2015."]

    tables = load_collection("herox")
    for question in queries:
        q = Question(text=question, type="NUM")
        q.parse()

        q_match = False

        tuples = []
        for obj in q.nps.union(q.nes):
            tuples.extend(get_all_tuples(tables, obj))

        done_tuple = False
        for tuple in tuples:
            done_tuple = True
            print(tuple)
            table_name = tuple[0]
            rel_name = tuple[1][0]
            words = normalise(question).split()

            q_bow = flatten_without_labels({"bow": bow})

            X = np.hstack((1, mc.get(table_name,rel_name), hmi(question,rel_name), bow.convert_one_hot(q_bow)))
            prediction = (lr.predict([X]))
            print(prediction)
            if prediction[0] == 1:
                value = num(re.sub(r"[^0-9\.]+","",tuple[1][2].replace(",","")))

                match = False
                for number in q.numbers:
                    if threshold_match(number,value,0.15):
                        match = True
                        q_match = True

                if match:
                    print("Match")
                    break

        if done_tuple:
            print(question + " - we predict: " + str(q_match))
        else:
            print("No data to answer questions")




