from stanford.corenlpy import Annotation, SharedPipeline, CoreAnnotations, chunk, number_ne_types, compound, \
    SemanticGraphCoreAnnotations, TreeCoreAnnotations, nps_from_tree


class Question:
    def __init__(self,text,type,answer=None):
        self.text = text
        self.type = type
        self.nes = set()
        self.numbers = set()
        self.nps = set()

    def parse(self):
        doc = Annotation(self.text)
        SharedPipeline().getInstance().annotate(doc)


        for sentence in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
            sentence = doc.get(CoreAnnotations.SentencesAnnotation).get(sentence)

            nes = []
            numbers = []

            for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
                corelabel = sentence.get(CoreAnnotations.TokensAnnotation).get(i)
                numbers.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) in number_ne_types)
                nes.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) != "O" and not numbers[-1])

            dep_graph = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation)
            parse_tree = sentence.get(TreeCoreAnnotations.TreeAnnotation)

            self.nps.update(set(nps_from_tree(parse_tree)))


            compoundNes = set(chunk(sentence,compound(dep_graph,sentence,nes)))

            self.nes.update(set(chunk(sentence,nes)).union(compoundNes))
            self.numbers.update(chunk(sentence,numbers))

        print(self.nes)
        print(self.numbers)
        print(self.nps)