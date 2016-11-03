import csv


def read_table(filename,base="data/WikiTableQuestions"):
    header = []
    rows = []

    header_read = False
    filename = filename.replace(".csv",".tsv")
    with open(base+"/"+filename,"r") as table:
        has_header = csv.Sniffer().has_header(table.readline())
        table.seek(0)

        for line in csv.reader(table, delimiter="\t"):
            if has_header and not header_read:
                header = line
                header_read = True
            else:
                rows.append(line)
    return {header: header, rows:rows}
