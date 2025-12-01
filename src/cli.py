import argparse
from trivia import QuestionBank

def list_questions(bank: QuestionBank):
    qs = bank.get_all()
    if not qs:
        print("No questions yet. Add one with `--add`.")
        return
    for q in qs:
        print(f"[{q.id}] ({q.category}) {q.question} -> {q.answer}")

def add_question(bank: QuestionBank, question, answer, category):
    q = bank.add_question(question, answer, category)
    print(f"Added: [{q.id}] {q.question}")

# Main entry point for the CLI program
def main():
   
    bank = QuestionBank()
   
    print("Trivia CLI - interactive mode")
    while True:
        cmd = input("Commands: [l]ist, [a]dd, [q]uit, [s]earch > ").strip().lower()
        if cmd in ("q", "quit"):
            break
        if cmd in ("l", "list"):
            list_questions(bank)
        elif cmd in ("a", "add"):
            question = input("Question: ").strip()
            answer = input("Answer: ").strip()
            category = input("Category (press enter for General): ").strip() or "General"
            bank.add_question(question, answer, category)
            print("Added.")
        elif cmd in ("s", "search"):
            term = input("Search term: ").strip()
            matches = bank.find(term)
            for q in matches:
                print(f"[{q.id}] ({q.category}) {q.question} -> {q.answer}")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
