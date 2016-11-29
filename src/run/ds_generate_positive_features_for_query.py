import os
import pickle
import sys
import re

from distant_supervision.clean_html import get_text, has_text
from distant_supervision.numbers_in_text import numbers_in_text, sentences_with_numbers
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.utterance_detection import find_utterances_for_tuple, matches_to_features

def num(s):
    try:
        return int(s.replace(",",""))
    except ValueError:
        return float(s.replace(",",""))


def contains_entity(text, entity):
    return True


if __name__ == "__main__":
    world = sys.argv[1]

    block = None
    if len(sys.argv) == 3:
        block = int(sys.argv[2])-1




    base = "data/distant_supervision/features/"

    if not os.path.exists(base):
        print("creating dir " + base)
        os.makedirs(base)

    found_urls = []
    with open("data/distant_supervision/queries_"+world+".txt", "r") as file:
        lines = file.readlines()
        num_qs = len(lines)

        if block is not None:
            lines = lines[block*100:min((block+1)*100,num_qs-1)]

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
                    print(" ")
                    print("Looking in document for values similar to " + target)
                    print(url)
                    text = get_text(url)

                    if len(text) == 0:
                        print("No meaningful text in this document")
                        continue

                    text = re.sub(r"\[[0-9]+\]", r"", text)

                    for number in target.strip().split("–"):
                        if number is None or len(number) == 0:
                            continue

                        filename = url_hash(url + "__" + search + "__" + number + "__" + table) + ".p"

                        if os.path.exists(base+filename):
                            continue

                        if contains_entity(text,entity):
                            #print(numbers_in_text(text))
                            sentences = sentences_with_numbers(text,num(number),0.15)
                            if len(sentences) == 0:
                                continue


                            print(str(len(sentences))+" candidate matches")
                            print(sentences)

                            try:
                                matches = find_utterances_for_tuple(sentences,
                                                                    {"entity": entity, "relation": relation})

                                features = matches_to_features(matches, num(number))

                                for feature in features:
                                    print("Target " + str(num(number)) + "\t\tActual " + str(
                                        feature['value']) + "\t\tClass\t\t" + str(
                                        feature["class"]))
                                print(features)
                                with open(base + filename, 'wb+') as f:
                                    pickle.dump(features, f)
                            except:
                                print(sys.exc_info()[0])
                                raise






"""
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
                continue
            else:
                entity = query[2].split("\" \"")[0][1:]

            for url in found_urls:
                text = get_text(url)

                if len(text) == 0:
                    continue

                text = re.sub(r"\[0-9+\]", "", text)

                if(entity_in_tex)
                print(text)
                print("")

"""