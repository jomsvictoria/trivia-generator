# Python Trivia Generator App

A small trivia application that:
- stores trivia questions locally (JSON)
- serves questions via a Flask API (easy to expose via `ngrok`)
- provides a CLI to view/add questions
- organized with object-oriented code (Question, QuestionBank)
- ready for Git/GitHub collaboration
- includes a unit test example

---

## Quick start

### Prerequisites
- Python 3.10+ recommended
- git
- (optional) ngrok — if you want to expose the local Flask server to the internet

### Setup
```bash
# clone
git clone <your-repo-url>
cd trivia-generator

# create venv (recommended)
python -m venv .venv
# activate (Windows)
# .venv\Scripts\activate
# mac / linux
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# serve FLASK api
python src/api.py

# open another terminal and run app on cli
python src/cli.py

For detailed API documentation, see [API Documentation](API_DOCUMENTATION.md)