import re
import sys

from classifier.LogisticRegressionClassifier import LogisticRegressionClassifier
from classifier.features.generate_features import FeatureGenerator, num
from distant_supervision.utterance_detection import f_threshold_match
from factchecking.question import Question
from tabular.filtering import load_collection

if __name__ == "__main__":
    fg = FeatureGenerator()
    Xs,ys = fg.generate_training()

    classifier = LogisticRegressionClassifier()
    classifier.train(Xs,ys)

    queries = ["Hamas was founded in 1985",
               "12.9% of the total population of the USA were daily smokers in 2014","97% of children in America were vaccinated against measles in 2014","In the USA there were 2.4 practicing doctors for every 1000 people in 2010"]

    tables = load_collection("herox")

    for q in queries:
        print(q)
        question = Question(text=q, type="NUM")
        tuples,q_features = fg.generate_test(tables,question)

        q_match = False

        if len(tuples)>0:
            q_predicted = classifier.predict(q_features)

            for i in range(len(tuples)):
                tuple = tuples[i]
                if len(tuple[1][2]) > 0:
                    prediction = q_predicted[i]
                    features = q_features[i]


                    if prediction == 1:
                        print(str(tuple) + "\t\t" + ("Match" if prediction else "No match"))
                        for number in question.numbers:
                            value = num(re.sub(r"[^0-9\.]+", "", tuple[1][2].replace(",", "")))

                            if value is None:
                                continue

                            if f_threshold_match(number, value, 0.05):
                                q_match = True

                        for number in question.dates:
                            value = num(re.sub(r"[^0-9\.]+", "", tuple[1][2].replace(",", "")))
                            if number == value:
                                q_match = True

            print(question.text)
            print(q_match)

        else:
            print(question.text)
            print("No supporting information can be found in the knowledge base")
        print("\n\n")
