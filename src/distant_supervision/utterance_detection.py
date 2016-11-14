import sys
from fuzzywuzzy import fuzz, process

from distant_supervision.stop_words import StopWords
from distant_supervision.strategy.relation_matching import exact_or_fuzzy_match_no_stopwords, stanford_normaliser
from stanford.corenlpy import SharedPipeline, Annotation, CoreAnnotations, CorefChainAnnotation, Integer






def find_utterances_for_tuple(lines, obj, relation_match_strategy=exact_or_fuzzy_match_no_stopwords):
    tokens = []

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

    possible_matches = []

    new_lines = []
    #process.extract(obj['relation'],"\n".join(lines).split(),scorer=fuzz.token_sort_ratio)
    for sentence_id in range(doc.get(CoreAnnotations.SentencesAnnotation).size()):
        sentence = doc.get(CoreAnnotations.SentencesAnnotation).get(sentence_id)

        incoref = False

        tokens = []

        for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = sentence.get(CoreAnnotations.TokensAnnotation).get(i)
            #print(corelabel.get(CoreAnnotations.TextAnnotation))



            coref = False
            mention = None
            for ref in entity_chain.getMentionsInTextualOrder().toArray():
                if sentence_id + 1 == ref.sentNum and i+1 >= ref.startIndex and i+1 < ref.endIndex:
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

        a = relation_match_strategy(tokens, sentence, obj['entity'])
        b = relation_match_strategy(tokens, sentence, obj['relation'])

        possible_matches.extend(set(a).intersection(b))

    possible_matches = set(possible_matches)
    return possible_matches


def extract_from_match(matches,number_matching_strategy=stanford_normaliser, numeric_only=True):



    for match in matches:
        numbers = number_matching_strategy(match)
        for i in range(match.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = match.get(CoreAnnotations.TokensAnnotation).get(i)
            print(corelabel.get(CoreAnnotations.TextAnnotation))


if __name__ == "__main__":
    passage = []

    for line in open("data/distant_supervision/scraped_texts/0c5988c0ec2256d525f0d648d01a9fa56e614a30ee03dcbcc22168039b603c0d.txt","r"):
        passage.append(line.strip())

    print(passage)
    sys.exit(1)

    passage.append("There were 2,000,000.53 dollars in the 19th prize fund")


    matches = find_utterances_for_tuple(passage, {"entity":"Mečíř","relation":"improved further in"})
    extract_from_match(matches)
