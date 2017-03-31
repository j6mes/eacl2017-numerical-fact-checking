from factchecking.quiz import Quiz

class PracticeQuiz(Quiz):
    def __init__(self,questions,answers):
        super().__init__(questions)
        self.answers = answers

    def answers(self):
        return self.answers