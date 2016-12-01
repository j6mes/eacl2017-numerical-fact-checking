from collections import defaultdict

from distant_supervision.query_generation import normalise, normalise_keep_nos
from tabular.table_collection import TableCollection
from tabular.table_filtering.filter_nes import FilterTableNEs
from tabular.table_filtering.filter_nes_memoized import FilterTableNEsMemoized
from tabular.table_reader import read_table, number_entity_tuples, table_nes
from wikitablequestions.dataset_reader import load_instances


def load_collection(name, filtering_strategy=FilterTableNEsMemoized):
    instances = load_instances(name)
    filtering = filtering_strategy()

    for instance in instances:
        filtering.register(instance['table'])

    return filtering


def write_collection(name,tables,base="data/WikiTableQuestions/data/"):
    with open(base+name+".tsv","w+") as f:
        f.write("id\tutterance\ttable\tvalue\n")
        id = 0

        for table in tables:
            f.write("f-"+str(id)+"\tNone\t"+table+"\tNone\n")
            id += 1



if __name__ == "__main__":
    instances = load_instances("herox")
    filtering = FilterTableNEsMemoized()

    for instance in instances:
        file = instance['table']
        filtering.register(file)

    print(filtering.get_tables("world life expectancy"))

