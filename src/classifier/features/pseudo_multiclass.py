from classifier.features.bow import BOW


class PseudoMultiClass():

    def __init__(self):
        self.headers = BOW()

    def join(self,table,header):
        raise Exception("Not implemented")

    def register(self,table,header):
        self.headers.register(self.join(table,header))

    def get(self,table,header):
        return self.headers.convert_one_hot([self.join(table,header)])[1:]


class IDPerTableMultiClass(PseudoMultiClass):
    def join(self,table,header):
        return table+"$$$"+header


class IDPerColumnMultiClass(PseudoMultiClass):
    def join(self,table,header):
        return header
