from tabular.table_reader import read_table


class TableCollection():
    def __init__(self):
        self.tables = dict()

    def load(self,table):
        if not table in self.tables:
            self.tables[table] = read_table(table)
        return self.tables[table]

    tc = None
    def instance():
        if TableCollection.tc is None:
            TableCollection.tc = TableCollection()
        return TableCollection.tc

    instance = staticmethod(instance)


if __name__ == "__main__":
    tc = TableCollection.instance()
    print(tc.load('csv/202-csv/281.csv'))
