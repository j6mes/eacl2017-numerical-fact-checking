import sys

number_ne_types = ['NUMBER','DURATION','MONEY','TIME','PERCENT','DATE']

def chunk(annotations,option):
    last_ne = []
    chunked_nes = []
    for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
        if(i>0):
            if(option[i-1]):
                if(option[i]):
                    last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))

                else:
                    if (len(last_ne)>0):
                        chunked_nes.append(" ".join(last_ne))
                        last_ne = []
            else:
                if(option[i]):
                    last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))

        else:
            if (option[i]):
                last_ne.append(annotations.get(CoreAnnotations.TokensAnnotation).get(i).get(CoreAnnotations.TextAnnotation))


    if (len(last_ne) > 0):
        chunked_nes.append(" ".join(last_ne))

    return chunked_nes




def compound(dep_graph,annotations,tagged):
    compound_nes = tagged

    changed = 1
    while changed > 0:
        changed = 0

        for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
            token = annotations.get(CoreAnnotations.TokensAnnotation).get(i)

            iterator = dep_graph.edgeIterable().iterator()

            while(iterator.hasNext()):
                edge = iterator.next()


                if(edge.getGovernor().index() == edge.getDependent().index()):
                    continue

                if(edge.getGovernor().index()-1 == i and compound_nes[edge.getGovernor().index()-1]):
                    if(edge.getRelation().getShortName() in ['compound','amod','nummod']):
                        if not compound_nes[edge.getDependent().index()-1] == compound_nes[edge.getGovernor().index()-1]:
                            changed +=1

                        compound_nes[edge.getDependent().index()-1] = compound_nes[edge.getGovernor().index()-1]

                elif (edge.getGovernor().index()-1 == i and compound_nes[edge.getDependent().index()-1]):
                    if(edge.getRelation().getShortName() in ['compound','amod','nummod']):
                        if not compound_nes[edge.getGovernor().index()-1] == compound_nes[edge.getDependent().index()-1]:
                            changed +=1

                        compound_nes[edge.getGovernor().index()-1] = compound_nes[edge.getDependent().index()-1]


    return compound_nes



from jnius import autoclass


Properties = autoclass("java.util.Properties")
StanfordCoreNLP = autoclass("edu.stanford.nlp.pipeline.StanfordCoreNLP")
CoreAnnotations = autoclass("edu.stanford.nlp.ling.CoreAnnotations")

CoreAnnotations.TokensAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TokensAnnotation")
CoreAnnotations.SentencesAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$SentencesAnnotation")
CoreAnnotations.TextAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TextAnnotation")
CoreAnnotations.NamedEntityTagAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NamedEntityTagAnnotation")

CoreAnnotations.NumericValueAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NumericTypeAnnotation")

CoreLabel = autoclass("edu.stanford.nlp.ling.CoreLabel")
IndexedWord = autoclass("edu.stanford.nlp.ling.IndexedWord")
Annotation = autoclass("edu.stanford.nlp.pipeline.Annotation")
SemanticGraph = autoclass("edu.stanford.nlp.semgraph.SemanticGraph")

SemanticGraphCoreAnnotations = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations")
SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations$CollapsedCCProcessedDependenciesAnnotation")

SemanticGraphEdge = autoclass("edu.stanford.nlp.semgraph.SemanticGraphEdge")
CoreMap = autoclass("edu.stanford.nlp.util.CoreMap")

NumberNormalizer = autoclass("edu.stanford.nlp.ie.NumberNormalizer")



class SharedPipeline:
    pipeline = None

    def __init__(self):
        if self.pipeline is None:
            props = Properties()
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref")

            pipeline = StanfordCoreNLP(props)
            self.pipeline = pipeline

    def getInstance(self):
        return self.pipeline


class SharedNERPipeline:
    pipeline = None

    def __init__(self):
        if self.pipeline is None:
            props = Properties()
            props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner")

            pipeline = StanfordCoreNLP(props)
            self.pipeline = pipeline

    def getInstance(self):
        return self.pipeline