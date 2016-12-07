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

    queries = ["Hamas was founded in 1985","In America, in June 1901, the average temperature was 16.6C","The World life expectancy was 52 in 1960", "world life expectancy rose sharply to 80 in 2014",
               "In 2012 there were 3,282,570 bee colonies in America","In 2016, the USA contributed $550bn to the financial intermediary funds","In the USA in 2010, the number of homicides by firearm was almost 10,000",
               "12.9% of the total population of the USA were daily smokers in 2014","97% of children in America were vaccinated against measles in 2014","In the USA there were 2.4 practicing doctors for every 1000 people in 2010"]

    tables = load_collection("herox")

    for q in queries:
        question = Question(text=q, type="NUM")
        tuples,q_features = fg.generate_test(tables,question)

        q_match = False

        if len(tuples)>0:
            q_predicted = classifier.predict(q_features)

            for i in range(len(tuples)):
                tuple = tuples[i]
                prediction = q_predicted[i]
                features = q_features[i]

                if prediction == 1:
                    for number in question.numbers:
                        value = num(re.sub(r"[^0-9\.]+", "", tuple[1][2].replace(",", "")))

                        if value is None:
                            continue

                        if f_threshold_match(number, value, 0.05):
                            print(tuple)
                            q_match = True

            if q_match:
                print(question.text)
                print(q_match)


        else:
            print(question.text)
            print("No supporting information can be found in the knowledge base")
        print("\n\n")
