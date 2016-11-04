import os

from distant_supervision.query_generation import generate_queries
from wikitablequestions.dataset_reader import load_instances
from wikitablequestions.table_reader import number_entity_tuples, read_table

if __name__=="__main__":
    all_instances = []

    all_instances.extend(load_instances("pristine-seen-tables"))
    all_instances.extend(load_instances("pristine-unseen-tables"))
    all_instances.extend(load_instances("training"))

    table_files = []

    done = 0
    for instance in all_instances:
        table_files.append(instance['table'])

    table_files = set(table_files)

    with open("data/distant_supervision/queries.txt", "w+") as file:
        for table_file in table_files:
            done += 1
            print("Parsing " + str(done) +"/"+str(len(table_files)) + "\t\t\t" + table_file)
            table = number_entity_tuples(read_table(table_file))
            tuples = generate_queries(table)


            for tuple in tuples:
                file.write(table_file + "\t" + tuple + "\n")
            file.flush()
            os.fsync(file.fileno())

