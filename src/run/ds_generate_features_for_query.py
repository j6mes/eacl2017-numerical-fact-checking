import os
import pickle
import sys

from distant_supervision.clean_html import get_text, has_text
from distant_supervision.scraper import url_hash
from distant_supervision.search import Search
from distant_supervision.utterance_detection import find_utterances_for_tuple, matches_to_features

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

                        print(filename)
                        if has_text(url):
                            text = get_text(url)


                            if len(text) == 0:
                                continue

                            matches = find_utterances_for_tuple(text.split("\n"),
                                                                    {"entity": entity, "relation": relation})

                            features = matches_to_features(matches, num(target))
                            for feature in features:
                                print("Target "+str(num(target))+"\t\tActual " + str(feature['value']) + "\t\tClass\t\t" + str(
                                    feature["class"]))
                            print (features)
                            with open(base+filename, 'wb+') as f:
                                pickle.dump(features, f)

                            print(str(100 * done / num_qs) + "%")
                        else:
                            print("Url is missing from file system and not downloaded")

                except:
                    pass