from factchecking.question import Question
from tabular.filtering import load_collection
from tabular.tuples import get_all_tuples

queries = ["Exxon Mobil reached a total value of $772 million in 2007.", "Around 90,000 unaccompanied children claimed asylum in the EU in 2015."]

tables = load_collection("herox")
for question in queries:
    q = Question(text=question,type="NUM")
    q.parse()

    tuples = []
    for obj in q.nps.union(q.nes):
        tuples.extend(get_all_tuples(tables, obj))

    print(tuples)





    print(q.numbers)


