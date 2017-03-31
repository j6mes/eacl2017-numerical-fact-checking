import itertools
import re

from classifier.features.generate_features import is_num
from factchecking.question import Question
from tabular.table_reader import read_table, number_entity_tuples
from wikitablequestions.dataset_reader import load_instances
from distant_supervision.normalisation import normalise


def key_terms(text):
    if type(text) != Question:
        question = Question(text, None)
        question.parse()
    else:
        question = text

    terms = []
    terms.extend(itertools.chain.from_iterable(ne.split() for ne in question.nes))
    terms.extend(itertools.chain.from_iterable(number.split() for number in question.numbers))
    terms.extend(itertools.chain.from_iterable(np.split() for np in question.nps))
    return set(terms)


def generate_search_query_known_table(text,table):
    terms = set(normalise(w) for w in key_terms(text))
    table = read_table(table)

    header_words = set(itertools.chain.from_iterable(normalise(h).split() for h in table['header']))

    print(header_words)
    print(terms)
    if len(header_words.intersection(terms)) > 0:
        print ("intersect")


    for row in table['rows']:
        print(table['header'])
        print(row)
        for cell in row:
            print(cell)
            if set(normalise(cell).split()).intersection(terms):
                print("MATCH")
                print(table['header'][row.index(cell)])
                print(cell)


def generate_query(tuple,filters=list()):

    datebit = ""
    if 'date' in tuple.keys():
        datebit = " " + " " .join(tuple['date'])

    if not is_num(tuple['value']):
        return None

    qry = tuple['value'] + "\t\""+tuple['entity'].replace("\\n", " ") + "\" " + tuple['relation'].replace("\\n", " ") + " " + datebit

    return qry


def generate_queries(tuples,filters=list()):
    return set(generate_query(tuple) for tuple in tuples if generate_query(tuple,filters) is not None)

if __name__ == "__main__":
    #generate_search_query_known_table("in what year did miss pokhara last win the miss nepal award","csv/204-csv/172.csv")
    all_instances = load_instances("training")
    all_instances.extend(load_instances("pristine-seen-tables"))

    table_files = []
    tuples = []


    done = 0
    for instance in all_instances:
        table_files.append(instance['table'])

    table_files = set(table_files)

    for table_file in table_files:
        done += 1
        print("Parsed " + str(done) +"/"+str(len(table_files)))
        table = number_entity_tuples(read_table(table_file))
        tuples.extend(generate_queries(table))


        if done > 100:
            break




    for tuple in tuples:
        print (tuple)

    print (len(tuples))





