from classifier.LogisticRegressionClassifier import LogisticRegressionClassifier
from classifier.features.generate_features import FeatureGenerator, num, is_num
from distant_supervision.utterance_detection import f_threshold_match
from factchecking.question import Question
from tabular.filtering import load_collection
import sys
import os

portion = 0
if len(sys.argv) > 1:
    portion = int(sys.argv[1])

fg = FeatureGenerator()
Xs,ys = fg.generate_training("emnlp")

classifier = LogisticRegressionClassifier()
classifier.train(Xs,ys)

import csv

base = "data/emnlp"
rels = []


tables = load_collection("emnlp")

from collections import defaultdict
import re


def fact_check_and_test(q, rel):
    question = Question(text=q, type="NUM")
    tuples, q_features = fg.generate_test(tables, question)
    q_match = False

    matches = dict()

    p_match = 0.0
    found_match = False
    total_geq = 0
    total_gt = 0
    total_match = 0

    entities = set()
    if len(tuples) > 0:
        for i in range(len(tuples)):

            tuple = tuples[i]
            skip = False
            if 'date' in tuple[1].keys() and len(question.dates):
                for date in question.dates:
                    dstrs = set()
                    for d in question.dates:
                        dstrs.add(str(d))
                    if not len(set(tuple[1]['date']).intersection(dstrs)):
                        skip = True

            if skip or not is_num(tuple[1]['value']):
                continue

            entities.add(tuple[1]['entity'])
            matches[tuple[1]['entity'] + "-----" + tuple[1]['relation']] = (tuple, q_features[i])

    if len(matches.keys()) > 0:
        for i in matches.keys():

            tuple = matches[i][0]
            features = matches[i][1]
            q_predicted = classifier.predict([features])

            skip = False
            if 'date' in tuple[1].keys() and len(question.dates):
                for date in question.dates:
                    dstrs = set()
                    for d in question.dates:
                        dstrs.add(str(d))
                    if not len(set(tuple[1]['date']).intersection(dstrs)):
                        skip = True

            if skip or not is_num(tuple[1]['value']):
                continue

            prediction = q_predicted[0][0]

            if prediction == 1:

                if (tuple[1]['relation'] == rel):
                    p_match = q_predicted[1][0][1]
                    found_match = True

    else:
        return (-1, 0, 0)

    if found_match:
        for i in matches.keys():

            tuple = matches[i][0]
            features = matches[i][1]
            q_predicted = classifier.predict([features])

            skip = False
            if 'date' in tuple[1].keys() and len(question.dates):
                for date in question.dates:
                    dstrs = set()
                    for d in question.dates:
                        dstrs.add(str(d))
                    if not len(set(tuple[1]['date']).intersection(dstrs)):
                        skip = True

            if skip or not is_num(tuple[1]['value']):
                continue

            prediction = q_predicted[0][0]

            if prediction == 1:
                if not (tuple[1]['relation'] == rel):
                    if q_predicted[1][0][1] > p_match:
                        total_gt += 1
                    if q_predicted[1][0][1] >= p_match:
                        total_geq += 1
                    total_match += 1

    if found_match:
        print("matched - ")
        print(total_gt)
        print(total_geq)
        print(total_match)
        return (1, total_gt, total_match, total_geq)

    rs = set()
    for tuple in tuples:
        if not is_num(tuple[1]['value']):
            pass
        rs.add(tuple[1]['relation'])

    if rel not in rs:
        return (-1, 0, 0, 0)
    return (0, 0, 0, 0)



files = []
for filename in os.listdir(base):
    if filename.endswith(".tsv"):
        files.append(filename)



portions = dict()
portions[0] = [0,1,2,3]
portions[1] = [4]
portions[2] = [5,6,7,8]
portions[4] = [9,10,11,12]
portions[5] = range(13,len(files))


if portion>0:
    for filename in files[portions[portion-1]]:
        with open(base + "/" + filename, encoding="ISO-8859-1") as tsv:
            for line in tsv.readlines():
                row = line.split("\t")
                if (len(row) == 12) and len(row[5].strip()) > 0:
                    if (row[0].lower().strip() != "n"):
                        rels.append({"entity": row[2], "relation": row[5]})
                elif len(row) == 10 and len(row[3].strip()) > 0:
                    rels.append({"entity": row[0], "relation": row[3]})
else:
    for filename in files:
        with open(base + "/" + filename, encoding="ISO-8859-1") as tsv:
            for line in tsv.readlines():
                row = line.split("\t")
                if (len(row) == 12) and len(row[5].strip()) > 0:
                    if (row[0].lower().strip() != "n"):
                        rels.append({"entity": row[2], "relation": row[5]})
                elif len(row) == 10 and len(row[3].strip()) > 0:
                    rels.append({"entity": row[0], "relation": row[3]})

property_names = dict()

property_names['fertility_rate'] = "Fertility rate, total (births per woman)"
property_names['gdp_growth_rate'] = "GDP growth (annual %)"
property_names['gdp_nominal_per_capita'] = "GDP per capita (current US$)"
property_names['gni_per_capita_in_ppp_dollars'] = "GNI per capita, PPP (current international $)"
property_names['life_expectancy'] = "Life expectancy at birth, total (years)"
property_names['cpi_inflation_rate'] = "Inflation, consumer prices (annual %)"
property_names['consumer_price_index'] = "Consumer price index (2010 = 100)"
property_names['diesel_price_liter'] = "Pump price for diesel fuel (US$ per liter)"
property_names['gni_in_ppp_dollars'] = "GNI (current US$)"
property_names['population_growth_rate'] = "Population growth (annual %)"
property_names['prevalence_of_undernourisment'] = "Prevalence of undernourishment (% of population)"
property_names['renewable_freshwater_per_capita'] = "Renewable internal freshwater resources per capita (cubic meters)"
property_names['health_expenditure_as_percent_of_gdp'] = "Health expenditure, total (% of GDP)"
property_names['internet_users_percent_population'] = "Internet users (per 100 people)"

tested = defaultdict(int)
results = defaultdict(int)
pr = defaultdict(int)

num_better = defaultdict(int)
num_total = defaultdict(int)
num_better_or_equal = defaultdict(int)

print(len(rels))

for rel in rels:
    rel['entity'] = re.sub('<[^<]+?>', '', rel['entity'])

    print("Testing " + rel['entity'])
    result = fact_check_and_test(rel['entity'], property_names[rel['relation']])
    if result[0] == 1:
        results[rel['relation']] += 1
        if result[1] == 0:
            pr[rel['relation']] += result[3]
        num_better[rel['relation']] += result[1]
        num_better_or_equal[rel['relation']] += result[3]
        num_total[rel['relation']] += result[2]

    if result[0] != -1:
        tested[rel['relation']] += 1

    print(result)

for key in tested.keys():
    print(key + " " + str(results[key]) + " " + str(num_better[key]) + " " + str(num_better_or_equal[key]) + " " + str(num_total[key]) + " " + str(pr[key]) + " " + str(tested[key]) + " " + str(results[key] / tested[key]))
