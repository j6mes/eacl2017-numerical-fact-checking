import csv
import os

from util import normalise,vocab, vocab_ngrams

from feature_eng import character_ngram
from TableQuestionAnswerTuple import TableQuestionAnswerTuple
from sklearn.linear_model import LogisticRegression

import sys

experiment_bow = int(sys.argv[1])
experiment_ngrams = int(sys.argv[2])

print("Running experiment " + str(experiment_bow)+ "-"+str(experiment_ngrams))



train = []
#
try:
    os.mkdir("out")
except:
    pass


with open("WikiTableQuestions/data/training.tsv") as tsv:
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
        train.append(TableQuestionAnswerTuple(line[0],line[1],line[2],line[2]))
        vocab.update(normalise(line[2]).split())
        vocab_ngrams.update(character_ngram(normalise(line[2])))

        print (line)

for obj in train:
    obj.load()
    for words in obj.header:
        vocab.update(normalise(words).split())
        vocab_ngrams.update(character_ngram(normalise(words)))

test = []
with open("WikiTableQuestions/data/pristine-unseen-tables.tsv") as tsv:
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
        test.append(TableQuestionAnswerTuple(line[0],line[1],line[2],line[2]))
        print (line)

for obj in test:
    obj.load()



trainingExamples = []
testExamples = []
print ("vocab size is "+str(len(vocab)))

done = 0
for obj in train:
    trainingExamples.append(obj.generateFeaturesForCorrect())
    trainingExamples.extend(obj.generateFeaturesForIncorrect(train))
    done+=1

    if(done%1000 == 0):
        print ("Load Training Example " + str(done))


lr = LogisticRegression()

Xs = []
ys = []
for ex in trainingExamples:
    Xs.append(ex[0])
    ys.append(ex[1])



tp = 0
fp = 0
fn = 0

done = 0


rankFile = open("out/rank."+str(experiment_bow)+"."+str(experiment_ngrams)+".csv","w+")

id = 0
for obj in test:
    id+=1

    testExamples = []
    testExamples.append(obj.generateFeaturesForCorrect())
    testExamples.extend(obj.genAll(test))


    done+=1

    print ("Load Test Example " + str(done))

    X_ts = []
    y_ts = []
    for ex in testExamples:
        X_ts.append(ex[0])
        y_ts.append(ex[1])

    lr.fit(Xs,ys)

    y_preds = lr.predict(X_ts)
    probs = lr.predict_proba(X_ts)


    print (obj.header)
    print (obj.question)



    if(y_preds[y_ts==1] == 1):
        tp += 1
        print ("found")


    cntWhereHigher = 0

    for i in range(0,len(probs[y_preds==1])):
        if(probs[y_ts==1][1]<probs[i][1]):
            cntWhereHigher+=1

    print (str(cntWhereHigher) + " tables were higher ranked")

    rankFile.write(str(id)+","+str(cntWhereHigher)+"\n")
    rankFile.flush()
    os.fsync(rankFile.fileno())

    fp += cntWhereHigher
 #       fp += len(y_preds[y_ts<y_preds])  #true values is 0 and y_preds =1
    fn += len(y_preds[y_ts>y_preds])


    print ("Precision (Global): " + str(tp/(tp+fp)))
    print ("Recall (Global): " + str(tp/(tp+fn)))

    print ("")
    print ("")

rankFile.close()
