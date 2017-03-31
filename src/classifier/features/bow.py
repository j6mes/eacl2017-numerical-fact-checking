import numpy as np

class BOW():
    def __init__(self):
        self.words = set()

    def register(self,word):
        if type(self.words) == list:
            if word in self.words:
                return

        self.words.add(word)

    def id(self,word):
        if type(self.words) == set:
            self.words = list(self.words)

        if word in self.words:
            return self.words.index(word)
        else:
            return -1

    def get_ids(self,array):
        ids = []

        for word in array:
            ids.append(self.id(word))

        return ids

    def convert_one_hot(self,array):
        # unknown word takes the first position
        fresh = np.zeros(len(self.words)+1)
        for id in self.get_ids(array):
            fresh[id+1] = 1

        return fresh


    def convert_counts(self,array):
        # unknown word takes the first position
        fresh = np.zeros(len(self.words)+1)
        for id in self.get_ids(array):
            fresh[id+1] += 1

        return fresh


if __name__ == "__main__":

    bow = BOW()

    bow.register("cat")
    bow.register("dog")
    bow.register("mouse")
    bow.register("lion")

    print(bow.get_ids(["cat","mouse","banana"]))
    print(bow.convert_counts(["cat","mouse","banana"]))
    print(bow.convert_counts(["cat","mouse"]))