import json

class Quiz:
    def __init__(self, quizzes_data, quiz_name):
        self.quizzes = quizzes_data  # Store the entire quizzes_data structure
        self.quiz_names = list(quizzes_data.keys())  # Get the list of quiz names

        # Initialize dictionaries to store questions, answers, and correct answers for the specified quiz
        self.questions = {}
        self.answers = {}
        self.correct_answers = {}

        if quiz_name in quizzes_data:
            quiz_data = quizzes_data[quiz_name]

            quiz_questions = {}
            quiz_answers = {}
            quiz_correct_answers = {}

            for question_key, question_data in quiz_data.items():
                # Store question text
                quiz_questions[question_key] = question_data["question"]

                # Store answers
                answers = question_data["answers"]
                for i, answer in enumerate(answers, start=1):
                    answer_key = f"A{question_key[-1]}_{i}"
                    quiz_answers[answer_key] = answer

                # Store correct answer
                correct_answer = question_data["correct_answer"]
                correct_answer_key = f"Correct_{question_key}"
                quiz_correct_answers[correct_answer_key] = correct_answer

            # Store questions, answers, and correct answers for the specified quiz
            self.questions[quiz_name] = quiz_questions
            self.answers[quiz_name] = quiz_answers
            self.correct_answers[quiz_name] = quiz_correct_answers
