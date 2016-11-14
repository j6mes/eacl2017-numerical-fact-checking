
class StopWords:

    sw = None

    words = set()
    def __init__(self):
        with open("data/distant_supervision/stopwords.txt") as file:
            for line in file:
                self.words.add(line.strip())

    def instance():
        if StopWords.sw is None:
            StopWords.sw = StopWords()

        return StopWords.sw

    instance = staticmethod(instance)