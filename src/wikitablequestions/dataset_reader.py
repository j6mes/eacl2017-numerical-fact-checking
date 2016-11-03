import csv


def load_instances(file,path="data/WikiTableQuestions/data"):
    instances = []

    with open(path+"/"+file+".tsv") as tsv:
        #Skip first line of TSV file if there is a header
        has_header = csv.Sniffer().has_header(tsv.read(1024))
        tsv.seek(0)
        reader = csv.reader(tsv, dialect="excel-tab")
        if has_header:
            next(reader)

        #Then read tsv table
        #col-1 - id
        #col-2 - NL utterance
        #col-3 - table
        #col-4 - answer

        for line in reader:
            instances.append({"id":line[0],"utterance":line[1],"table":line[2], "answer":line[3]})

    return instances
