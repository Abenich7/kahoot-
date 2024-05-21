import json

# Initialize the quiz database
quiz_database = {"quizzes": []}

def create_quiz(quiz_name, quiz_level, category, date_written):
    """
    Function to create a new quiz and add it to the quiz database.
    """
    new_quiz = {
        "quizName": quiz_name,
        "quizLevel": quiz_level,
        "category": category,
        "dateWritten": date_written,
        "numQuestions": 0,  # Initially set to 0, will be updated later
        "timeToSolve": None,  # Placeholder, to be calculated later
        "questions": []
    }
    quiz_database["quizzes"].append(new_quiz)
    return new_quiz

def add_question(quiz, question, answers, correct_answer, time_to_solve=None):
    """
    Function to add a new question to an existing quiz.
    """
    new_question = {
        "q": question,
        "answers": answers,
        "timeToSolve": time_to_solve,
        "correct": correct_answer
    }
    quiz["questions"].append(new_question)
    quiz["numQuestions"] += 1  # Increment the number of questions
    return new_question

# Example usage:
# Create a new quiz
new_quiz = create_quiz(
    quiz_name="New Quiz",
    quiz_level="medium",
    category=["category1", "category2"],
    date_written="02.03.2024"
)

# Add questions to the new quiz
add_question(
    quiz=new_quiz,
    question="What is Python?",
    answers={"a1": "A programming language", "a2": "A snake", "a3": "A fruit", "a4": "A car"},
    correct_answer="a1"
)

add_question(
    quiz=new_quiz,
    question="Who created Python?",
    answers={"a1": "Guido van Rossum", "a2": "Steve Jobs", "a3": "Bill Gates", "a4": "Mark Zuckerberg"},
    correct_answer="a1"
)

# Convert the quiz database to JSON string
quiz_json = json.dumps(quiz_database, indent=4)

# Print the JSON string
print(quiz_json)