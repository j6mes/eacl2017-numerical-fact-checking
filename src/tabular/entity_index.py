from tabular.table_reader import read_table


def generate_index(tables):
    for table in tables:
        table = read_table(table)
