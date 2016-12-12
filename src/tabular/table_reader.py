import csv
import numpy as np
import re
from stanford.corenlpy import *


def transpose(l):
    return list(map(list, zip(*l)))


def read_table(filename, base="data/WikiTableQuestions"):
    header = []
    rows = []

    header_read = False
    filename = filename.replace(".csv", ".tsv")
    with open(base + "/" + filename, "r", encoding='utf-8') as table:
        has_header = csv.Sniffer().has_header(table.readline())
        table.seek(0)

        for line in csv.reader(table, delimiter="\t"):
            if has_header and not header_read:
                header = line
                header_read = True
            else:
                rows.append(line)
    return {"header": header, "rows": rows}


def table_nes(table):
    header = table['header']
    rows = table['rows']

    ret_tokens = []
    for col in transpose(rows):
        text = ". ".join(col)
        doc = Annotation(text)
        SharedNERPipeline().getInstance().annotate(doc)

        num_ne_cell = 0
        tokens = []
        for cell in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            col = doc.get(CoreAnnotations.SentencesAnnotation).get(cell)

            words = []
            col_ne_tags = []
            has_ne = False
            for i in range(col.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = col.get(CoreAnnotations.TokensAnnotation).get(i)
                ne = corelabel.get(CoreAnnotations.NamedEntityTagAnnotation)

                words.append(corelabel.get(CoreAnnotations.TextAnnotation))
                if ne not in ['O', 'NUMBER', 'NUMERIC']:
                    has_ne = True

            if len(words) > 1:
                tokens.append(" ".join(words[:-1]))

            if has_ne:
                num_ne_cell += 1

        if num_ne_cell >= len(tokens) / 2 and len(tokens) > 0:
            ret_tokens.extend(tokens)

    return ret_tokens


def number_tuples(table):
    header = table['header']
    rows = table['rows']

    ret_tokens = []
    entity_col = []
    date_col = []
    number_col = []

    col_id = 0

    table_trans = transpose(rows)
    for col in table_trans:

        text = ". ".join(col)
        doc = Annotation(text)
        SharedNERPipeline().getInstance().annotate(doc)

        num_ne_cell = 0
        num_date_cell = 0
        num_number_cell = 0

        tokens = []
        for cell in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            col = doc.get(CoreAnnotations.SentencesAnnotation).get(cell)

            words = []
            col_ne_tags = []
            has_ne = False
            has_date = False
            has_number = False
            for i in range(col.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = col.get(CoreAnnotations.TokensAnnotation).get(i)
                ne = corelabel.get(CoreAnnotations.NamedEntityTagAnnotation)

                words.append(corelabel.get(CoreAnnotations.TextAnnotation))
                if ne not in ['O', 'NUMBER', 'NUMERIC', 'DATE', 'YEAR']:
                    has_ne = True

                if ne in ['YEAR', 'DATE']:
                    has_date = True

                if ne in ['NUMBER', 'NUMERIC', 'PERCENTAGE', 'ORDINAL']:
                    has_number = True

            if len(words) > 1:
                tokens.append(" ".join(words[:-1]))

            if has_ne:
                num_ne_cell += 1

            if has_date:
                num_date_cell += 1

            if has_number:
                num_number_cell += 1

        if num_ne_cell >= len(tokens) / 2 and len(tokens) > 0:
            entity_col.append(col_id)

        if num_date_cell >= len(tokens) / 2 and len(tokens) > 0:
            number_col.append(col_id)

        if num_number_cell >= len(tokens) / 2 and len(tokens) > 0:
            number_col.append(col_id)

        col_id += 1

    tuples = []
    for col in entity_col:
        for col1 in number_col:
            tuples.extend(list(zip([header[col1]] * len(rows), table_trans[col], table_trans[col1])))

    return tuples



def number_entity_tuples(table):
    header = table['header']
    rows = table['rows']

    text = ". ".join(" ".join(cell for cell in row) for row in transpose(rows))

    doc = Annotation(text)
    SharedNERPipeline().getInstance().annotate(doc)

    ne_columns = []
    number_columns = []
    for column in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
        col = doc.get(CoreAnnotations.SentencesAnnotation).get(column)


        tokens = []
        col_ne_tags = []
        for i in range(col.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = col.get(CoreAnnotations.TokensAnnotation).get(i)
            tokens.append(corelabel.get(CoreAnnotations.TextAnnotation))
            col_ne_tags.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation))

        tags = col_ne_tags


        for tag in tags:
            if len(set(col_ne_tags).intersection(set(number_ne_types))) == 0 and tag not in ['NUMBER','NUMERIC','YEAR','DATE','DURATION','TIME','NUMBER','ORDINAL'] and tag != "O":
                ne_columns.append(column)
                break


        count_in = 0
        if column not in ne_columns:
            for tag in tags:
                if tag in number_ne_types:
                    count_in += 1

            if count_in >= len(tags)/2:
                number_columns.append(column)

    numbers = []


    tuples = []
    transposed = transpose(rows)
    for column in range(len(transposed)):
        if column in ne_columns:
            for ncolumn in range(len(transposed)):
                if ncolumn in number_columns:
                    tuples.extend(list(zip([header[ncolumn]] * len(rows),transposed[column],transposed[ncolumn])))


    return tuples


def number_entity_date_tuples(table):
    header = table['header']
    rows = table['rows']

    ret_tokens = []
    entity_col = []
    date_col = []
    number_col = []

    col_id = 0

    table_trans = transpose(rows)
    for col in table_trans:

        text = ". ".join(col)
        doc = Annotation(text)
        SharedNERPipeline().getInstance().annotate(doc)

        num_ne_cell = 0
        num_date_cell = 0
        num_number_cell = 0

        tokens = []
        for cell in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            col = doc.get(CoreAnnotations.SentencesAnnotation).get(cell)

            words = []
            col_ne_tags = []
            has_ne = False
            has_date = False
            has_number = False
            for i in range(col.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = col.get(CoreAnnotations.TokensAnnotation).get(i)
                ne = corelabel.get(CoreAnnotations.NamedEntityTagAnnotation)

                words.append(corelabel.get(CoreAnnotations.TextAnnotation))
                if ne not in ['O', 'NUMBER', 'NUMERIC', 'DATE', 'YEAR']:
                    has_ne = True

                if ne in ['YEAR', 'DATE']:
                    has_date = True

                if ne in ['NUMBER', 'NUMERIC', 'PERCENTAGE', 'ORDINAL']:
                    has_number = True

            if len(words) > 1:
                tokens.append(" ".join(words[:-1]))

            if has_ne:
                num_ne_cell += 1

            if has_date:
                num_date_cell += 1

            if has_number:
                num_number_cell += 1

        if num_ne_cell >= len(tokens) / 2 and len(tokens) > 0:
            entity_col.append(col_id)

        if num_date_cell >= len(tokens) / 2 and len(tokens) > 0:
            date_col.append(col_id)

        if num_number_cell >= len(tokens) / 2 and len(tokens) > 0:
            number_col.append(col_id)

        col_id += 1

    tuples = []
    for col in entity_col:
        for col1 in number_col:
            extra = []
            if len(date_col) > 0:
                for dc in date_col:
                    extra.append(table_trans[dc])
                extra = transpose(extra)
                tuples.extend(list(zip([header[col1]] * len(rows), table_trans[col], table_trans[col1], extra)))
            else:
                tuples.extend(list(zip([header[col1]] * len(rows), table_trans[col], table_trans[col1])))

    return tuples




if __name__ == "__main__":
    t = read_table("herox/5.csv")
    print(number_entity_tuples(t))