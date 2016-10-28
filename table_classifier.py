from data_reader import *

import sys
import os
import numpy as np
import random
from sklearn.linear_model import LogisticRegression

random.seed(12345)


def train(train_file,kb=None):
    print("Loading Training Data")
    train = load_instances(train_file,add_to_global_bow=True)
    trainingExamples = []

    Xs = []
    ys = []
    done = 0
    for instance in train:
        # AV: The naming is a bit odd: shouldn't all question-table pairs have the same features?
        trainingExamples.append(instance.generateFeaturesForCorrect())
        # AV: You probably want to refactor this; why pick only one randomly, and not all?
        # AV: Or even better, pick to generate a negative training example using a table
        # that is more likely to be useful, e.g. one that has high overlap?
        trainingExamples.extend(instance.generateFeaturesForIncorrect(train))

        done += 1
        if (done % 1000 == 0):
            print("Load Training Example " + str(done))

    for ex in trainingExamples:
        Xs.append(ex[0])
        ys.append(ex[1])

    lr = LogisticRegression()

    print("Training log reg classifier")
    lr.fit(Xs, ys)

    if(kb is not None):
        kb.extend(train)


    #Return the logistic regression classifier
    return lr


def evaluate(lr, test_file, kb=None):
    try:
        os.mkdir("out")
        print("Created output directory for results")
    except:
        pass

    experiment_bow = int(sys.argv[1])
    experiment_ngrams = int(sys.argv[2])
    rankFile = open("out/rank."+str(experiment_bow)+"."+str(experiment_ngrams)+".csv","w+")

    print("Loading Test Data")
    test = load_instances(test_file)

    if (kb is not None):
        kb.extend(test)

    tp = 0
    fp = 0
    fn = 0

    done = 0
    id = 0

    #Iterate over every table in the test set
    for obj in test:
        print("Load Test Example " + str(done))

        id += 1

        testExamples = []
        # AV: I see what you do mean here, but it assumes that you know the correct answer
        # Of course, you don't actually use it, but would be better to have genAll do what it says
        # Updated it genAll to this effect.
        # testExamples.append(obj.generateFeaturesForCorrect())

        # That's fine. There was a need for the correct value to be first, that no longer exists
        testExamples.extend(obj.genAll(test))

        done += 1

        X_ts = []  # feature vector for all test examples
        y_ts = []  # class for all test examples (1 - is correct, 0 - is not correct)
        for ex in testExamples:
            X_ts.append(ex[0])
            y_ts.append(ex[1])

        X_ts = np.array(X_ts)
        y_ts = np.array(y_ts)

        # predict class for each example and record probabilities
        y_preds = lr.predict(X_ts)
        y_probs = lr.predict_proba(X_ts)

        print("question:", obj.question)
        print("correct table:", obj.table_path)
        print("header", obj.header)

        found_flag = 0
        # AV: Not sure I get this: y_preds an array of the predctions whether each table is good
        # for the question. y_ts is also an array which is compared to an integer? This will
        # always return 0, thus this evaluates whether the first table considered is the correct one?


        # JT: y_ts==1 will return a vector where the 'correct' table is True and all other values is false
        # Use y_preds[y_ts==1] will return the predicted class for the entry where the true label is 1.
        # When this value is also 1, then we can record a true positive match. - this worked on python2 and has
        # been fixed for python3 thanks to numpy
        if (y_preds[y_ts == 1][0] == 1):
            tp += 1
            found_flag = 1
            print("found")

        # JT: Again, use this y_ts==1 index to identify the number of tables which have a higher probability than the
        # probability given by classifying the correct entry
        cntWhereHigher = 0
        for i in range(0, len(y_probs[y_preds == 1])):
            if (y_probs[y_ts == 1][0][1] < y_probs[i][1]):
                cntWhereHigher += 1
        print(str(cntWhereHigher) + " tables were higher ranked")
        rankFile.write(str(id) + "," + str(cntWhereHigher) + "," + str(found_flag) + "\n")
        rankFile.flush()
        os.fsync(rankFile.fileno())

        # Number of false positives is number of entries that scored higher than the actual
        fp += cntWhereHigher

        # Number of false negatives is the number of predicted entries where an entry should be classified as 1
        # but is instead is ranked 0. Use the > apply this behaviour the the list
        fn += len(y_preds[y_ts > y_preds])

        print("Precision (Global): " + str(tp / (tp + fp)))
        print("Recall (Global): " + str(tp / (tp + fn)))

        print("")
        print("")

    rankFile.close()



def runtime_predict(question,tables,classifier):
    q = TableQuestionAnswerTuple(None,question,None,None)
    q.gen_q_features()

    kb = q.genAll(tables)
    Xs = []

    for item in kb:
        Xs.append(item[0])

    y_pred = np.array(classifier.predict(Xs))

    kb=np.array(kb)

    print(y_pred)
    print(kb[y_pred==1])


if __name__ == "__main__":
    classifier = train("training")
    evaluate(classifier,"pristine-unseen-tables")



