from itertools import groupby
from operator import itemgetter

from stanford.corenlpy import CoreAnnotations, SemanticGraphCoreAnnotations


class Match():

    def __init__(self,sentence, entity_name, number_pos, date_pos, coref_pos, entity_pos):
        self.sentence = sentence
        self.entity_name = entity_name

        self.numbers = []
        self.number_pos = []
        for k, g in groupby(enumerate(number_pos), lambda t: t[0] - t[1]):
            number_pos_grouped = (map(itemgetter(1), g))
            n_pos = []
            number_utterance = []
            for pos in number_pos_grouped:
                n_pos.append(pos)
                number_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))
            self.number_pos.append(n_pos)
            self.numbers.append(number_utterance)

        self.dates = []
        self.date_pos = []
        for k, g in groupby(enumerate(date_pos), lambda t: t[0] - t[1]):
            date_pos_grouped = (map(itemgetter(1), g))
            date_pos = []
            date_utterance = []
            for pos in date_pos_grouped:
                date_pos.append(pos)
                date_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))
            self.date_pos.append(date_pos)
            self.dates.append(date_utterance)


        self.entity = []
        self.entity_pos = []
        for k, g in groupby(enumerate(entity_pos), lambda t: t[0] - t[1]):
            entity_coref_grouped = (map(itemgetter(1), g))
            e_pos = []
            entity_utterance = []
            for pos in entity_coref_grouped:
                e_pos.append(pos)
                entity_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))
            self.entity_pos.append(e_pos)
            self.entity.append(entity_utterance)

        self.entity_coref = []
        self.entity_coref_pos = []
        for k, g in groupby(enumerate(coref_pos), lambda t: t[0] - t[1]):
            entity_coref_pos_grouped = (map(itemgetter(1), g))

            coref_utterance = []
            coref_pos = []
            for pos in entity_coref_pos_grouped:
                coref_pos.append(pos)
                coref_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))
            self.entity_coref_pos.append(coref_pos)
            self.entity_coref.append(coref_utterance)

    def complete_bow(self,pair):
        r = self.get_internal_index_span(pair[0], pair[1])

        words = self.get_span_bow(r)
        return words

    def get_features(self, ffun = {complete_bow}):
        pairs = self.get_feature_pairs()

        all_features = []

        for pair in pairs:
            features= dict()

            if pair[2]:
                features["type"] = "number"
            else:
                features["type"] = "date"

            features["entity"] = self.entity_name
            features["entity_utterance"] = " ".join(self.sentence.get(CoreAnnotations.TokensAnnotation).get(e).get(CoreAnnotations.TextAnnotation) for e in pair[0])
            features["value"] = [self.sentence.get(CoreAnnotations.TokensAnnotation).get(e).get(CoreAnnotations.NumericCompositeValueAnnotation) for e in pair[1]]

            try:
                for feature_function in ffun:
                    features[feature_function.__name__] = feature_function(self,pair)
            except:
                continue

            all_features.append(features)
        return all_features



    def get_span_bow(self,range):
        tokens = []
        for pos in range:
            tokens.append(self.sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

        return tokens


    def get_feature_pairs(self):
        pairs = []
        for entity in self.entity_coref_pos:
            for number in self.number_pos:
                pairs.append((entity,number,True))

            for date in self.date_pos:
                pairs.append((entity, date,False))

        for entity in self.entity_pos:
            for number in self.number_pos:
                if len(list(number)) is not 0 and len(list(entity)) is not 0:
                    pairs.append((entity,number,True))

            for date in self.date_pos:
                if len(list(date)) is not 0 and len(list(entity)) is not 0:
                    pairs.append((entity, date,False))


        return pairs

    def get_internal_index_span(self,entity1,entity2):
        if max(entity1) < min(entity2):
            return range(max(entity1)+1,min(entity2))

        if min(entity1) > max(entity2):
            return range(max(entity2)+1,min(entity1))

        if not set(entity1).isdisjoint(set(entity2)):
            raise AssertionError("Entity sets are not disjoint")

    def get_complete_index_span(self,entity1,entity2):
        if max(entity1) < min(entity2):
            return range(max(entity1),min(entity2)+1)

        if min(entity1) > max(entity2):
            return range(max(entity2),min(entity1)+1)

        if not set(entity1).isdisjoint(set(entity2)):
            raise AssertionError("Entity sets are not disjoint")


    def get_words_between_indices(self,start,end):
        pass