# 代码生成时间: 2025-10-10 19:46:33
# coding: utf-8
# Smart Question Bank System using Falcon Framework

from falcon import API, Request, Response
import json

# Define the question bank data structure
QUESTION_BANK = {
    "1": {"question": "What is the capital of France?", "answer": "Paris"},
    "2": {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    "3": {"question": "What is the chemical symbol for water?", "answer": "H2O"},
}

# Define the resource for handling questions
class QuestionBankResource:
    def on_get(self, req, resp):
        """
        Handle GET requests to retrieve questions.
        Returns a list of questions from the question bank.
        """
        try:
            # Retrieve all questions from the question bank
            questions = QUESTION_BANK.values()
            resp.media = list(questions)
            resp.status = falcon.HTTP_200
        except Exception as e:
            # Handle any unexpected errors
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        """
        Handle POST requests to add new questions to the question bank.
        """
        try:
            # Get the new question from the request body
            new_question = req.media
            # Generate a unique ID for the new question
            question_id = str(len(QUESTION_BANK) + 1)
            # Add the new question to the question bank
            QUESTION_BANK[question_id] = new_question
            resp.media = {"success": f"Question added with ID {question_id}"}
            resp.status = falcon.HTTP_201
        except KeyError as e:
            # Handle missing fields in the request body
            resp.media = {"error": f"Missing field: {str(e)}"}
            resp.status = falcon.HTTP_400
        except Exception as e:
            # Handle any unexpected errors
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500

# Initialize the Falcon API
api = API()

# Add the QuestionBankResource to the API
api.add_route("/questions", QuestionBankResource())