from fuzzywuzzy import fuzz, process

from stanford.corenlpy import SharedPipeline, Annotation, CoreAnnotations, CorefChainAnnotation, Integer


def find_utterances_for_tuple(lines, obj, numeric_only=True):
    doc = Annotation("\n".join(lines))
    SharedPipeline().getInstance().annotate(doc)

    coref_map = doc.get(CorefChainAnnotation)

    entity_chain = None
    relation_chain = None
    for chain in range(coref_map.size()):
        ch = coref_map.get(Integer(chain + 1))

        if ch is not None:
            word = ch.getRepresentativeMention().mentionSpan

            if fuzz.partial_ratio(word, obj['entity']) > 85:
                entity_chain = ch
                break

    for chain in range(coref_map.size()):
        ch = coref_map.get(Integer(chain + 1))

        if ch is not None:
            word = ch.getRepresentativeMention().mentionSpan

            if fuzz.partial_ratio(word, obj['relation']) > 85:
                relation_chain = ch
                break



    for sentence_id in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
        sentence = doc.get(CoreAnnotations.SentencesAnnotation).get(sentence_id)

        incoref = False
        tokens = []
        for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = sentence.get(CoreAnnotations.TokensAnnotation).get(i)

            coref = False
            mention = None
            for ref in entity_chain.getMentionsInTextualOrder().toArray():
                if sentence_id + 1 == ref.sentNum and ref.startIndex >= i+1 and i+1 <= ref.endIndex:
                    coref = True
                    mention = ref
                    break

            if coref:
                if not incoref:
                    tokens.append(obj['entity'])
                    incoref = True
            else:
                incoref = False
                tokens.append(corelabel.get(CoreAnnotations.TextAnnotation))


        print(tokens)

if __name__ == "__main__":
    passage = []

    for line in open("data/distant_supervision/scraped_texts/0c5988c0ec2256d525f0d648d01a9fa56e614a30ee03dcbcc22168039b603c0d.txt","r"):
        passage.append(line.strip())


    find_utterances_for_tuple(passage, {"entity":"Mečíř","relation":"improved further in"})
