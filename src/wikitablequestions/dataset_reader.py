import csv

import sys


def load_instances(file,path="data/WikiTableQuestions/data",has_header=True):
    instances = []


    with open(path+"/"+file+".tsv") as tsv:
        read_header = False
        #Skip first line of TSV file if there is a header
        #has_header = csv.Sniffer().has_header(tsv.read(2048))
        tsv.seek(0)
        reader = csv.reader(tsv, dialect="excel-tab")

        #Then read tsv table
        #col-1 - id
        #col-2 - NL utterance
        #col-3 - table
        #col-4 - answer

        for line in reader:
            if has_header and not read_header:
                read_header = True
                continue

            instances.append({"id":line[0],"utterance":line[1],"table":line[2], "answer":line[3]})

    return instances
