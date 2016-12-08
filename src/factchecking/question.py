
from distant_supervision.numbers_in_text import numbers_in_text
from stanford.corenlpy import Annotation, SharedPipeline, CoreAnnotations, chunk, number_ne_types, compound, \
    SemanticGraphCoreAnnotations, TreeCoreAnnotations, nps_from_tree, NumberNormalizer, chunk_num, num


class Question:
    def __init__(self,text,type,answer=None):
        self.text = text
        self.type = type
        self.nes = set()
        self.numbers = set()
        self.dates = set()
        self.nps = set()

    def parse(self):
        doc = Annotation(self.text)
        SharedPipeline().getInstance().annotate(doc)


        for sentence in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            sentence = doc.get(CoreAnnotations.SentencesAnnotation).get(sentence)

            tokens = []
            nes = []
            numbers = []
            dates = []
            for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = sentence.get(CoreAnnotations.TokensAnnotation).get(i)
                tokens.append(corelabel.get(CoreAnnotations.TextAnnotation))
                numbers.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) in number_ne_types)
                dates.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) in ["DATE","YEAR"])
                nes.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) != "O" and not numbers[-1] and not dates[-1])

            dep_graph = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation)
            parse_tree = sentence.get(TreeCoreAnnotations.TreeAnnotation)

            self.nps.update(set(nps_from_tree(parse_tree)).difference(set(numbers)))


            compoundNes = set(chunk(sentence,compound(dep_graph,sentence,nes)))

            self.nes.update(set(chunk(sentence,nes)).union(compoundNes))

            for i in range(len(tokens)):
                if dates[i]:
                    self.dates.add(num(tokens[i]))

            self.numbers.update(numbers_in_text(self.text))
            self.numbers = self.numbers.difference(self.dates)

            a = self.numbers
            self.numbers = set()
            for b in a:
                self.numbers.add(num(b))


