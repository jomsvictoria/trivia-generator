import json
import uuid
from typing import List, Optional, Dict
from pathlib import Path
import tempfile
import os

# ----------------------------------------
# DATA FILE LOCATION
# DATA_PATH points to: trivia-generator/questions.json
# 
# __file__ = this file's path
# resolve() = absolute path
# parent.parent = go 2 folders up
# ----------------------------------------
DATA_PATH = Path(__file__).resolve().parent.parent / "questions.json"


# ======================================================
# Question Model
# Represents a single trivia question
# ======================================================
class Question:
    def __init__(self, question: str, answer: str, category: str = "General", id: Optional[int] = None):
        self.id = id  # will be assigned by QuestionBank.add_question()
        self.question = question
        self.answer = answer
        self.category = category
    # Convert object → dictionary (used for JSON saving)
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category
        }

    # Create a Question object from a dictionary (used when loading from JSON)
    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            question=d["question"],
            answer=d["answer"],
            category=d.get("category", "General"),
            id=d.get("id")   # optional, so it doesn't generate a new one
        )
# ======================================================
# QuestionBank
# Stores, loads, searches, and saves all questions
# ======================================================
class QuestionBank:
    def __init__(self, storage_path: Optional[Path] = None):
        self.next_id = 1
        self.storage_path = Path(storage_path) if storage_path else DATA_PATH
        self.questions: List[Question] = []
        self._load() # Load JSON file on startup

    # ----------------------------------------
    # Load questions.json into memory
    # ----------------------------------------
    def _load(self):
        if not self.storage_path.exists():
            self.questions = []
            self.next_id = 1
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            # Convert each dict to Question object
            self.questions = [Question.from_dict(x) for x in raw]
            
            if self.questions:
                self.next_id = max(q.id for q in self.questions) + 1
            else:
                self.next_id = 1
                
        except Exception:
            self.questions = []
            self.next_id = 1
    # ----------------------------------------
    # Safely write JSON to disk using atomic write
    # Prevents data corruption if app crashes while writing
    # ----------------------------------------
    def _atomic_write(self, data):
        # write to a tempfile and rename for atomic replace
        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.storage_path.parent)
        try:
            # Write JSON data to temp file
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmpf:
                json.dump(data, tmpf, indent=2, ensure_ascii=False)
            # Replace original file with temp file
            os.replace(tmp_path, str(self.storage_path))
        except Exception:
            # Clean up temp file if write fails
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise  # rethrow error

    # Save all questions to the JSON file
    def save(self):
        data = [q.to_dict() for q in self.questions]
        self._atomic_write(data)
    # Add a new question
    def add_question(self, question_text: str, answer_text: str, category: str = "General") -> Question:
        q = Question(question_text, answer_text, category)
        
        q.id = self.next_id
        self.next_id += 1
        self.questions.append(q)
        self.save()
        
        return q
    # Get all questions as a list
    def get_all(self) -> List[Question]:
        return list(self.questions)
    # Get a question by ID
    def get_by_id(self, id: str) -> Optional[Question]:
        for q in self.questions:
            if q.id == id:
                return q
        return None
    
    # Search for questions containing a keyword
    # Looks at both question and answer text
    def find(self, term: str) -> List[Question]:
        term = term.lower()
        return [q for q in self.questions if term in q.question.lower() or term in q.answer.lower()]
    
    # Convert entire question bank to JSON-serializable list
    # Useful if API wants to return the raw list
    def to_json(self) -> List[Dict]:
        return [q.to_dict() for q in self.questions]
