# src/api.py
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from trivia import QuestionBank, Question


# ----------------------------------------
# Initialize Flask app and enable CORS
# CORS = allows API to be used by web apps
# ----------------------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------------------
# QuestionBank instance:
# This holds all the trivia questions in memory
# ----------------------------------------
bank = QuestionBank()

# ----------------------------------------
# ROOT ENDPOINT
# http://localhost:5000/
# A simple check that the API is running
# ----------------------------------------
@app.get("/")
def index():
    return jsonify({"status": "ok", "message": "Trivia API", "count": len(bank.get_all())})

# ----------------------------------------
# GET /questions
# Retrieve all questions.
# Supports optional filters:
#   - /questions?category=Science
#   - /questions?q=earth
# ----------------------------------------
@app.get("/questions")
def get_questions():
    # optional ?category= or ?q=search
    category = request.args.get("category")
    q = request.args.get("q")
    all_qs = bank.get_all()
    results = all_qs
    if category:
        results = [x for x in results if x.category.lower() == category.lower()]
    if q:
        results = [x for x in results if q.lower() in x.question.lower() or q.lower() in x.answer.lower()]
    return jsonify([x.to_dict() for x in results])

# ----------------------------------------
# GET /questions/<id>
# Retrieve a single question by its ID
# Example: /questions/abc123
# ----------------------------------------
@app.get("/questions/<id>")
def get_question(id):
    qobj = bank.get_by_id(id)
    if not qobj:
        abort(404, "Question not found")
    return jsonify(qobj.to_dict())

# Create a new trivia question
@app.post("/questions")
def create_question():
    data = request.get_json(force=True) # Force=True means even if no JSON header, try to parse JSON
    if not data:
        abort(400, "invalid json")
    # Extract fields
    question = data.get("question")
    answer = data.get("answer")
    category = data.get("category", "General")
    
    # Basic validation
    if not question or not answer:
        abort(400, "question and answer are required")
    # Add the new question to the bank
    q = bank.add_question(question, answer, category)
    return jsonify(q.to_dict()), 201

# ----------------------------------------
# Run the Flask server
# debug=True = automatic reload on file changes
# ----------------------------------------
if __name__ == "__main__":    
    app.run(host="0.0.0.0", port=5000, debug=True)
