from tabular.table_filtering.filter_nes_memoized import FilterTableNEsMemoized
from wikitablequestions.dataset_reader import load_instances

def load_collection(name, filtering_strategy=FilterTableNEsMemoized):
    instances = load_instances(name)
    filtering = filtering_strategy(name)

    for instance in instances:
        filtering.register(instance['table'])

    return filtering


def write_collection(name,tables,base="data/table/"):
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

