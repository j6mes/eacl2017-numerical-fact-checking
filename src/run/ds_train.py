import os
import pickle
import sys

from sklearn.linear_model import LogisticRegression

from classifier.features.bow import BOW
from classifier.features.linearise import flatten_with_labels, flatten_without_labels
from distant_supervision.clean_html import get_text, has_text
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.utterance_detection import find_utterances_for_tuple, matches_to_features

import numpy as np


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

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

                try:
                    urls = Search.instance().search(search)

                    for url in urls:
                        filename = url_hash(url + "__"+ search + "__" + target + "__" + table) + ".p"

                        if has_text(url) and os.path.exists(base+filename):
                            with open(base+filename, 'rb') as f:
                                features = pickle.load(f)

                                for feature in features:
                                    feature['table'] = table
                                    feature['relation'] = relation

                                found_features.extend(features)
                        else:
                            pass


                except SystemExit:
                    sys.exit(0)
                except:
                    break


    bow = BOW()
    for feature in found_features:
        words = (flatten_without_labels({"bow":feature['complete_bow']}))
        for word in words:
            bow.register(word)


    headers = BOW()
    for feature in found_features:
        headers.register(feature['relation'])


    Xs = []
    ys = []
    for feature in found_features:
        words = (flatten_without_labels({"bow": feature['complete_bow']}))
        X = np.hstack((1, headers.convert_one_hot([feature['relation']]), feature['header_match_intersection'], bow.convert_one_hot(words)))
        y = feature['class']

        Xs.append(X)
        ys.append(y)



    lr = LogisticRegression()
    lr.fit(Xs,ys)

