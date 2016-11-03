import itertools

from factchecking.question import Question
from wikitablequestions.table_reader import read_table


def key_terms(text):
    if type(text) != Question:
        question = Question(text, None)
        question.parse()
    else:
        question = text

    terms = []
    terms.extend(itertools.chain.from_iterable(ne.split() for ne in question.nes))
    terms.extend(itertools.chain.from_iterable(number.split() for number in question.numbers))
    terms.extend(itertools.chain.from_iterable(np.split() for np in question.nps))

    return set(terms)

def generate_search_query_known_table(text,table):
    terms = key_terms(text)
    table = read_table(table)

    header_words = set(itertools.chain.from_iterable(h.split() for h in table.header))
    if len(header_words.intersection(terms)) > 0:
        print ("intersect")



if __name__ == "__main__":
    generate_search_query_known_table("in what year did miss pokhara last win the miss nepal award two thousand","csv/204-csv/172.csv")




