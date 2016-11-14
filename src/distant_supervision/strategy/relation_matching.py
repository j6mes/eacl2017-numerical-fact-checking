from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from distant_supervision.stop_words import StopWords
from stanford.corenlpy import CoreAnnotations, NumberNormalizer


def exact_or_fuzzy_match(tokens,sentence,target):

    pos = 0
    for token in tokens:
        coreLabel = sentence.get(CoreAnnotations.TokensAnnotation).get(pos)

        while sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation) in StopWords.instance().words:
            print("stop word - " + sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

            if pos+1 < sentence.get(CoreAnnotations.TokensAnnotation).size():
                pos+=1
            else:
                break
            coreLabel = sentence.get(CoreAnnotations.TokensAnnotation).get(pos)

        print((token,coreLabel.get(CoreAnnotations.TextAnnotation)))
        pos +=1



    possible_matches = []
    if len(set(tokens).intersection(set(target.split()))) > 0:
        possible_matches.append(sentence)

    for fuzzy_match in process.extract(target, tokens, scorer=fuzz.token_sort_ratio):
        if fuzzy_match[1] > 85:
            possible_matches.append(sentence)

    return set(possible_matches)


def exact_or_fuzzy_match_no_stopwords(tokens,sentence,target):
    tokens_no_stop = []
    for token in tokens:
        if token not in StopWords.instance().words:
            tokens_no_stop.append(token)

    target_no_stop = []
    for token in target.split():
        if token not in StopWords.instance().words:
            target_no_stop.append(token)

    return exact_or_fuzzy_match(tokens_no_stop,sentence," ".join(target_no_stop))


def stanford_normaliser(sentence):
    numbers = []
    numbers_annotation = NumberNormalizer.findAndMergeNumbers(sentence)

    for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
        numbers.append(numbers_annotation.toArray()[i].get(CoreAnnotations.NumericCompositeValueAnnotation))

    return numbers