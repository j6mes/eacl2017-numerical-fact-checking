import re
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

