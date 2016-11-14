from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from distant_supervision.stop_words import StopWords
from stanford.corenlpy import CoreAnnotations, NumberNormalizer


def exact_or_fuzzy_match(tokens,sentence,target):
    match = False

    if len(set(tokens).intersection(set(target.split()))) > 0:
        match = True

    for fuzzy_match in process.extract(target, tokens, scorer=fuzz.token_sort_ratio):
        if fuzzy_match[1] > 85:
            match = True

    return match


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