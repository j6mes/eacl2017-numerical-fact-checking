import csv
import numpy as np
import re
from stanford.corenlpy import *


def transpose(l):
    return list(map(list, zip(*l)))


def read_table(filename, base="data/table"):
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

    hnums = set()
    hidx = 0
    for h in header:
        doc = Annotation(h)
        SharedNERPipeline().getInstance().annotate(doc)

        for s in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            c = doc.get(CoreAnnotations.SentencesAnnotation).get(s)
            for i in range(c.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = c.get(CoreAnnotations.TokensAnnotation).get(i)
                ne = corelabel.get(CoreAnnotations.NamedEntityTagAnnotation)

                if ne in ['YEAR', 'DATE']:
                    hnums.add(hidx)
        hidx += 1

    hseries = False
    if (len(hnums) >= len(header) / 2):
        hseries = True

    num_nes = []
    num_dates = []
    num_numbers = []

    all_tokens = []
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
                if ne not in ['O', 'NUMBER', 'NUMERIC', 'DATE', 'YEAR','PERCENTAGE', 'ORDINAL','DURATION','SET']:
                    has_ne = True

                if ne in ['YEAR', 'DATE']:
                    has_date = True

                if ne in ['NUMBER', 'NUMERIC', 'PERCENTAGE', 'ORDINAL']:
                    has_number = True

            if len(words) > 0:
                tokens.append(" ".join(words[:-1]))


            if has_ne:
                num_ne_cell += 1

            if has_date:
                num_date_cell += 1

            if has_number:
                num_number_cell += 1

        num_nes.append(num_ne_cell)
        num_dates.append(num_date_cell)
        num_numbers.append(num_number_cell)
        all_tokens.append(tokens)

    col_id = 0
    for col in table_trans:
        if num_nes[col_id] >= len(all_tokens[col_id]) / 2 and len(all_tokens[col_id]) > 0:
            entity_col.append(col_id)
        col_id += 1

    col_id = 0
    for col in table_trans:
        if len(entity_col) and num_dates[col_id] >= len(all_tokens[col_id]) / 2 and len(all_tokens[col_id]) > 0:
            if col_id < max(entity_col) and col_id > min(entity_col):
                number_col.append(col_id)
            else:
                date_col.append(col_id)

        if num_numbers[col_id] >= len(all_tokens[col_id]) / 2:
            number_col.append(col_id)
        col_id += 1

    tuples = []

    if not hseries:
        for col in entity_col:
            for col1 in number_col:
                if col1 in entity_col:
                    continue
                if col in number_col:
                    continue

                extra = []
                if len(date_col) > 0:
                    for dc in date_col:
                        extra.append(table_trans[dc])
                    extra = transpose(extra)
                # TODO entity/relation/value

                for i in range(len(rows)):
                    t = dict()
                    t['relation'] = header[col1]
                    t['value'] = table_trans[col1][i]
                    t['entity'] = table_trans[col][i]

                    if len(extra):
                        t['date'] = extra[i]
                    tuples.append(t)

    else:

        hnums = list(hnums)

        nh = (set(range(len(header))).difference(hnums))
        tr = []

        extra = []
        for col in nh:
            if col not in entity_col:
                extra.append(table_trans[col])
        el = len(extra)
        extra = transpose(extra)

        for hnum in hnums:
            for ecol in entity_col:
                l = list(zip([header[hnum]] * len(rows), table_trans[hnum], extra))
                i = 0
                for t in l:
                    for rel in t[2:][0]:
                        t2 = dict()

                        t2['entity'] = table_trans[ecol][i]
                        t2['relation'] = rel
                        for item in t[0:1]:
                            if 'date' not in t2:
                                t2['date'] = []
                            t2['date'].append(item)

                        t2['value'] = t[1]

                        tuples.append(t2)
                    i += 1

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