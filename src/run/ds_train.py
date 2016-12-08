import os
import pickle
import re
import sys
from collections import defaultdict

from sklearn.linear_model import LogisticRegression

from classifier.features.bow import BOW
from classifier.features.linearise import flatten_with_labels, flatten_without_labels
from classifier.features.pseudo_multiclass import IDPerColumnMultiClass
from distant_supervision.clean_html import get_text, has_text
from distant_supervision.query_generation import normalise_keep_nos
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.utterance_detection import find_utterances_for_tuple, matches_to_features, threshold_match, \
    f_threshold_match

import numpy as np

from factchecking.question import Question
from tabular.filtering import load_collection
from tabular.tuples import get_all_tuples


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None


def hmi(sentence, sentence1):
    return 1 if len(
        set(normalise_keep_nos(sentence).split()).intersection(set(normalise_keep_nos(sentence1).split()))) > 0 else 0

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
            print("Done: " + str(done*100/num_qs))

            done += 1
            query = line.replace("\n"," ").strip().split("\t")

            table = query[0]
            targets = query[1].strip().replace(",","").split("-")
            search = query[2]

            if search.split("\" \"")[1].replace("\"","").isnumeric():
                print("skipped")
                print (query)
            else:

                for target in targets:
                    entity = query[2].split("\" \"")[0][1:]
                    relation = query[2].split("\" \"")[1][:-1]

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




    print("Registering words in BOW")

    n_feats = len(found_features)
    done = 0
    bow = BOW()
    for feature in found_features:
        words = (flatten_without_labels({"bow":feature['complete_bow']}))
        for word in words:
            bow.register(word)
        done+=1
        if done%5000 == 0:
            print(str(done*100/n_feats)+ "%")


    print("Registering columns")
    mc = IDPerColumnMultiClass()
    for feature in found_features:
        mc.register(feature['table'],feature['relation'])



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

            if done%100 == 0:
                print(done)
            done += 1


            words = (flatten_without_labels({"bow": feature['complete_bow']}))
            X = np.hstack((1, mc.get(feature['table'],feature['relation']), feature['header_match_intersection'], bow.convert_one_hot(words)))

            Xs.append(X)
            ys.append(y)

    print("Subsampling negative features")
    done = 0
    num_incorrect = defaultdict(int)
    for feature in found_features:
        y = feature['class']

        if y == 0 and num_incorrect[feature['relation']] < num_correct[feature['relation']]:
            if done%100 == 0:
                print(done)
            done += 1


            num_incorrect[feature['relation']] += 1
            words = (flatten_without_labels({"bow": feature['complete_bow']}))
            X = np.hstack((1, mc.get(feature['table'],feature['relation']), feature['header_match_intersection'], bow.convert_one_hot(words)))

            Xs.append(X)
            ys.append(y)

    #pickle.dump(Xs, open("dump.x","w+"))
    #pickle.dump(ys, open("dump.y","w+"))
    #pickle.dump(bow.words,open("dump.bow","w+"))
    #pickle.dump(mc.headers.words,open("dump.mc","w+"))


    print("Training classifier")
    lr = LogisticRegression(penalty='l1',C=0.9)
    lr.fit(Xs,ys)

    import pickle
    s = pickle.dumps(lr)

    print(lr)

    print("Trained")


    queries = ["Hamas was founded in 1985","In America, in June 1901, the average temperature was 16.6C","The World life expectancy was 52 in 1960", "world life expectancy rose sharply to 80 in 2014",
               "In 2012 there were 3,282,570 bee colonies in America","In 2016, the USA contributed $550bn to the financial intermediary funds"]

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
            table_name = tuple[0]
            rel_name = tuple[1][0]
            words = normalise_keep_nos(question).split()

            q_bow = flatten_without_labels({"bow": bow})

            X = np.hstack((1, mc.get(table_name,rel_name), hmi(question,rel_name), bow.convert_one_hot(q_bow)))
            prediction = (lr.predict([X]))

            if prediction[0] == 1:
                value = num(re.sub(r"[^0-9\.]+","",tuple[1][2].replace(",","")))

                if value is None:
                    continue

                match = False
                for number in q.numbers:
                    if f_threshold_match(number,value,0.05):
                        match = True
                        q_match = True

                for number in q.dates:
                    if number==value:
                        match = True
                        q_match = True


                print(tuple)
                print(lr.predict_proba([X]))
                print(prediction)
                print("Match")



        if done_tuple:
            print(question + " - we predict: " + str(q_match))
        else:
            print("No data to answer questions")
        print("")
        print("")
        print("")
        print("")