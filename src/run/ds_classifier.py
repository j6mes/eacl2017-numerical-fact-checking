import re
from classifier.LogisticRegressionClassifier import LogisticRegressionClassifier
from classifier.features.generate_features import FeatureGenerator, num
from distant_supervision.utterance_detection import f_threshold_match
from factchecking.question import Question
from tabular.filtering import load_collection

def fact_check(q):
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
                    print(str(tuple) + "\t\t" + ("Possible Match" if prediction else "No match"))
                    for number in question.numbers:
                        value = num(re.sub(r"[^0-9\.]+", "", tuple[1][2].replace(",", "")))

                        if value is None:
                            continue

                        if f_threshold_match(number, value, 0.05):
                            print(str(tuple) + "\t\t" + "Threshold Match to 5%")
                            q_match = True

                    for number in question.dates:
                        value = num(re.sub(r"[^0-9\.]+", "", tuple[1][2].replace(",", "")))
                        if number == value:
                            print(str(tuple) + "\t\t" + "Exact Match")
                            q_match = True
        print(question.text)
        print(q_match)

    else:
        print(question.text)
        print("No supporting information can be found in the knowledge base")
    print("\n\n")


if __name__ == "__main__":
    fg = FeatureGenerator()
    Xs,ys = fg.generate_training()

    classifier = LogisticRegressionClassifier()
    classifier.train(Xs,ys)

    queries = ["Exxon Mobil reached a total value of $772 million in 2007","Around 90,000 unaccompanied children claimed asylum in the EU in 2015","Hamas was founded in 1985","In America, in June 1901, the average temperature was 16.6C","The World life expectancy was 52 in 1960", "world life expectancy rose sharply to 80 in 2014",
               "In 2012 there were 3,282,570 bee colonies in America","In 2016, the USA contributed $550bn to the financial intermediary funds"]

    tables = load_collection("herox")

    for q in queries:
        print(q)
        fact_check(q)
