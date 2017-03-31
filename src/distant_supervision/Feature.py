from itertools import groupby
from operator import itemgetter

from stanford.corenlpy import CoreAnnotations


class Feature():

    def __init__(self,sentence, number_pos, date_pos, coref_pos, entity_pos):
        self.sentence = sentence

        self.numbers = []
        for k, g in groupby(enumerate(number_pos), lambda t: t[0] - t[1]):
            number_pos_grouped = (map(itemgetter(1), g))
            self.number_pos = number_pos_grouped
            number_utterance = []
            for pos in number_pos_grouped:
                number_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

            self.numbers.append(number_utterance)

        self.dates = []
        for k, g in groupby(enumerate(date_pos), lambda t: t[0] - t[1]):
            date_pos_grouped = (map(itemgetter(1), g))
            self.date_pos = date_pos_grouped
            date_utterance = []
            for pos in date_pos_grouped:
                date_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

            self.dates.append(date_utterance)


        self.entity = []
        for k, g in groupby(enumerate(entity_pos), lambda t: t[0] - t[1]):
            entity_coref_grouped = (map(itemgetter(1), g))
            self.entity_pos = entity_coref_grouped
            entity_utterance = []
            for pos in entity_coref_grouped:
                entity_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

            self.entity.append(entity_utterance)

        self.entity_coref = []
        for k, g in groupby(enumerate(coref_pos), lambda t: t[0] - t[1]):
            entity_coref_pos_grouped = (map(itemgetter(1), g))
            self.entity_coref_pos = entity_coref_pos_grouped
            coref_utterance = []
            for pos in entity_coref_pos_grouped:
                coref_utterance.append(
                    sentence.get(CoreAnnotations.TokensAnnotation).get(pos).get(CoreAnnotations.TextAnnotation))

            self.entity_coref.append(coref_utterance)

    def get_feature_pairs(self):
        for entity in self.entity:
            for date in self.dates:
                Feature(entity,)

        print(self.entity)
        print(self.entity_coref)
        print(self.dates)
        print(self.numbers)