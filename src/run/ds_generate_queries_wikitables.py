import os
import sys

from distant_supervision.query_generation import generate_queries
from tabular.table_reader import read_table, number_tuples
from wikitablequestions.dataset_reader import load_instances

if __name__=="__main__":
    world = sys.argv[1]
    all_instances = []
    all_instances.extend(load_instances(world))
    table_files = []

    done = 0
    for instance in all_instances:
        table_files.append(instance['table'])

    table_files = set(table_files)

    with open("data/distant_supervision/queries_"+world +".txt", "w+") as file:
        for table_file in table_files:
            done += 1
            print("Parsing " + str(done) +"/"+str(len(table_files)) + "\t\t\t" + table_file)
            table = number_tuples(read_table(table_file))
            tuples = generate_queries(table)


            for tuple in tuples:
                file.write(table_file + "\t" + tuple + "\n")
            file.flush()
            os.fsync(file.fileno())

