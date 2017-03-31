class Answer:
    def factory(text):
        if text == "T":
            return TrueAnswer()
        elif text == "HT":
            return HalfTrueAnswer()
        elif text == "HF":
            return HalfFalseAnswer()
        elif text == "F":
            return FalseAnswer()

    factory = staticmethod(factory)


class TrueAnswer(Answer):
    pass

class HalfTrueAnswer(Answer):
    pass

class HalfFalseAnswer(Answer):
    pass

class FalseAnswer(Answer):
    pass
