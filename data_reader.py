import csv

from TableQuestionAnswerTuple import TableQuestionAnswerTuple
from feature_eng import character_ngram
from util import normalise, vocab_ngrams, vocab



def load_instances(file,add_to_global_bow=False):
    instances = []

    with open("WikiTableQuestions/data/"+file+".tsv") as tsv:
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
            instances.append(TableQuestionAnswerTuple(line[0],line[1],line[2],line[2]))

            #add input utterance to global BOWs
            if(add_to_global_bow):
                vocab.update(normalise(line[2]).split())
                vocab_ngrams.update(character_ngram(normalise(line[2])))

            print (line)

    #read table from disk
    for obj in instances:
        obj.load()

        # add table headers to global BOWs
        for words in obj.header:
            vocab.update(normalise(words).split())
            vocab_ngrams.update(character_ngram(normalise(words)))


    done = 0
    for obj in instances:
        obj.load_global()

        done+=1
        if(done%1000 == 0):
            print("Precomputing feature vectors - " + str(done))



    return instances
