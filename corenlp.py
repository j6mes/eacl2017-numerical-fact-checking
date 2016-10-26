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




def compound(dep_graph,tagged):
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







mytext = "Texas has 37 electoral votes."
number_ne_types = ['NUMBER','DURATION','MONEY','TIME','PERCENT','DATE']

from jnius import autoclass


Properties = autoclass("java.util.Properties")
StanfordCoreNLP = autoclass("edu.stanford.nlp.pipeline.StanfordCoreNLP")
CoreAnnotations = autoclass("edu.stanford.nlp.ling.CoreAnnotations")

CoreAnnotations.TokensAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TokensAnnotation")
CoreAnnotations.SentencesAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$SentencesAnnotation")
CoreAnnotations.TextAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$TextAnnotation")
CoreAnnotations.NamedEntityTagAnnotation = autoclass("edu.stanford.nlp.ling.CoreAnnotations$NamedEntityTagAnnotation")

CoreLabel = autoclass("edu.stanford.nlp.ling.CoreLabel")
IndexedWord = autoclass("edu.stanford.nlp.ling.IndexedWord")
Annotation = autoclass("edu.stanford.nlp.pipeline.Annotation")
SemanticGraph = autoclass("edu.stanford.nlp.semgraph.SemanticGraph")

SemanticGraphCoreAnnotations = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations")
SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation = autoclass("edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations$CollapsedCCProcessedDependenciesAnnotation")

SemanticGraphEdge = autoclass("edu.stanford.nlp.semgraph.SemanticGraphEdge")
CoreMap = autoclass("edu.stanford.nlp.util.CoreMap")



props = Properties()
props.setProperty("annotators","tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref")

pipeline = StanfordCoreNLP(props)
doc = Annotation(mytext)

pipeline.annotate(doc)

annotations = doc.get(CoreAnnotations.SentencesAnnotation).get(0)



nes = []
numbers = []

for i in range(annotations.get(CoreAnnotations.TokensAnnotation).size()):
    corelabel = annotations.get(CoreAnnotations.TokensAnnotation).get(i)
    numbers.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) in number_ne_types)
    nes.append(corelabel.get(CoreAnnotations.NamedEntityTagAnnotation) != "O" and not numbers[-1])


depgraph = annotations.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation)

entities = set(chunk(annotations,nes)).union(set(chunk(annotations,compound(depgraph,nes))))
nums = set(chunk(annotations,numbers))

print [(x,y) for x in entities for y in nums]


