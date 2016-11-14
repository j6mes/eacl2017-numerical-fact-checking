from stanford.corenlpy import CoreAnnotations


class Match():

    def __init__(self,sentence,entity_pos,rel_pos,num_pos):
        self.sentence = sentence

        entity =
        for i in range(sentence.get(CoreAnnotations.TokensAnnotation).size()):
            corelabel = sentence.get(CoreAnnotations.TokensAnnotation).get(i)

            if i in entity_pos: