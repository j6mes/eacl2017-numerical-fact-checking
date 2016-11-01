from factchecking.answer import Answer
from factchecking.practice_quiz import PracticeQuiz
from factchecking.question import Question
from factchecking.quiz import Quiz


def quiz_tsv_file(filename,root="data/herox/quiz"):
    with open(filename, 'r') as f:

        questions = []
        answers = []

        for line in f:
            line = line.replace("\n"," ").strip()
            bits = line.split("\t")

            question_type = bits[0]
            question = bits[1]

            answer = None
            if len(bits) > 2:
                answer = Answer.factory(bits[2])
                answers.append(answer)

            questions.append(Question(text=question,type=question_type,answer=answer))

        if len(questions) == len(answers):
            return PracticeQuiz(questions,answers)
        else:
            return Quiz(questions)

