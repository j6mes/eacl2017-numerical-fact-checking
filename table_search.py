import csv
import re

import sys

from stanford.corenlpy import SharedPipeline, Annotation, SharedNERPipeline, number_ne_types, CoreAnnotations, \
    NumberNormalizer

from TableQuestionAnswerTuple import TableQuestionAnswerTuple

def transpose(l):
    return list(map(list, zip(*l)))

def read_file(filename):
    rows = []
    header = []

    header_read = False
    with open("WikiTableQuestions/" + filename.replace(".csv", ".tsv")) as table:
        # check if header
        has_header = csv.Sniffer().has_header(table.readline())
        table.seek(0)

        for line in csv.reader(table, delimiter="\t"):
            if (has_header and not header_read):
                header = line
                header_read = True
            else:
                rows.append(line)
    return (header, rows)



def split_table(header,rows):
    text = ". ".join(" ".join(cell for cell in row) for row in transpose(rows))

    doc = Annotation(text)
    SharedNERPipeline().getInstance().annotate(doc)


    number_columns = []
    for column in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
        col = doc.get(CoreAnnotations.SentencesAnnotation).get(column)


        tokens = []
        col_ne_tags = []
        for i in range(col.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = col.get(CoreAnnotations.TokensAnnotation).get(i)
            tokens.append(corelabel.get(CoreAnnotations.TextAnnotation))
            col_ne_tags.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation))



        if len(set(col_ne_tags).intersection(set(number_ne_types)))>0:
            number_columns.append(column)

    numbers = []


    tuples = []
    transposed = transpose(rows)
    for column in range(len(transposed)):
        if column not in number_columns:
            for ncolumn in range(len(transposed)):
                if ncolumn in number_columns:
                    #print("next col")
                    numberlist = doc.get(CoreAnnotations.SentencesAnnotation).get(ncolumn)

                    #for number in range(numberlist.size()):
                    #    print (transposed[ncolumn][number])
                    #    try:
                    #        print (NumberNormalizer.wordToNumber(transposed[ncolumn][number]))
                    #    except:
                    #        nv = re.sub(r'[^0-9\.]','',transposed[ncolumn][number])
                    #        print(nv)
                    #        print (NumberNormalizer.wordToNumber(nv))
                        #print(str(numberlist.size())  + " ---- " +str(number))
                        #print (numberlist.get(CoreAnnotations.TokensAnnotation).get(number).get(CoreAnnotations.TextAnnotation))


                    tuples.extend(list(zip([header[ncolumn]] * len(rows),transposed[column],transposed[ncolumn])))

    return tuples




def search(filename,query,ne,num,search=read_file):
    print("Reading "+ filename)
    table = read_file(filename)
    return split_table(table[0],table[1])


def load_instances(file,add_to_global_bow=False):
    instances = []

    with open("WikiTableQuestions/data/"+file+".tsv") as tsv:
        #Skip first line of TSV file if there is a header
        has_header = csv.Sniffer().has_header(tsv.read(1024))
        tsv.seek(0)
        reader = csv.reader(tsv, dialect="excel-tab")
        if has_header:
            next(reader)

        #Then read tsv table
        #col-1 - id
        #col-2 - NL utterance
        #col-3 - table
        #col-4 - answer

        for line in reader:
            instances.append(line[2])

    return instances





if __name__ == "__main__":
    instances = load_instances('training')
    print(len(instances))

    if(int(sys.argv[1])>len(instances)):
        sys.exit()


    print(instances[int(sys.argv[1]) : min(int(sys.argv[1])+100,len(instances))])

    for instance in instances:
        tuples = (search(instance,None,None,None))
        with open("tuples/"+instance.replace('.csv','') +".tsv",'w+') as file:
            for tuple in tuples:
                file.write(tuple[0]+"\t"+tuple[1]+"\t"+tuple[2]+"\n")
        print("Generated " + str(len(tuples)) + " tuples")


    #search('csv/204-csv/410.csv','Who came after Cahill','Cahill',12))