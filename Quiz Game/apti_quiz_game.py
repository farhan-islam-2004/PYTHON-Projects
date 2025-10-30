import csv
import random
import threading
import datetime
import sys
import os

user_answer = None

def get_input():
    global user_answer
    user_answer = input("Your choice (1-4): ").strip()

def ask_question(question, options, correct, time_limit=30):
    global user_answer
    user_answer = None

    # Shuffle options but always renumber 1–4
    shuffled_opts = options[:]
    random.shuffle(shuffled_opts)

    # Find new index of the correct answer after shuffling
    correct_index = shuffled_opts.index(options[correct-1]) + 1

    print(f"\n⏳ You have {time_limit} seconds!")
    print("👉", question)
    for i, opt in enumerate(shuffled_opts, 1):
        print(f"{i}. {opt}")

    # Start input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout=time_limit)

    if user_answer is None:
        print("\n⏰ Time's up!")
        return False
    elif user_answer.isdigit() and int(user_answer) == correct_index:
        print("✅ Correct!")
        return True
    else:
        print(f"❌ Wrong! Correct answer: {shuffled_opts[correct_index-1]}")
        return False


def find_csv_file(filename):
    """Try to locate the CSV file in common places."""
    # 1. Path as given (could be absolute or relative to cwd)
    if os.path.isfile(filename):
        return os.path.abspath(filename)

    # 2. Downloads folder (Windows/Linux/Mac)
    home = os.path.expanduser("~")
    downloads_path = os.path.join(home, "Downloads", filename)
    if os.path.isfile(downloads_path):
        return downloads_path

    # 3. Script directory (where this file lives)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, filename)
        if os.path.isfile(script_path):
            return script_path

        # 4. Parent of script directory (in case project layout)
        parent_path = os.path.join(script_dir, os.pardir, filename)
        parent_path = os.path.abspath(parent_path)
        if os.path.isfile(parent_path):
            return parent_path
    except NameError:
        # __file__ may not be defined in some execution contexts; ignore
        pass

    # 5. Not found
    print(f"⚠️ Could not find the CSV file '{filename}' in cwd, Downloads, or the script folder.")
    print("Current working directory:", os.getcwd())
    print("Script directory (if available):", os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else 'unknown')
    sys.exit(1)

def load_questions_csv(filename):
    questions = []
    try:
        with open(filename, newline='', encoding="utf-8") as csvfile:
            # Dataset uses semicolon delimiter
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                q = row["Question"].strip()
                opts = [
                    row["Option A"].strip(),
                    row["Option B"].strip(),
                    row["Option C"].strip(),
                    row["Option D"].strip()
                ]
                # Convert Answer letter (A/B/C/D) to index (1–4)
                answer_letter = row["Answer"].strip().upper()
                mapping = {"A": 1, "B": 2, "C": 3, "D": 4}
                correct = mapping.get(answer_letter, None)

                if correct:
                    questions.append({
                        "category": "General Aptitude",   # dataset has no category column
                        "difficulty": "Medium",          # dataset has no difficulty column
                        "q": q,
                        "opts": opts,
                        "correct": correct
                    })
    except FileNotFoundError:
        print("⚠️ CSV file not found. Exiting...")
        sys.exit(1)
    return questions

def main():
    # Allow the user to pass a path as the first CLI argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "clean_general_aptitude_dataset.csv"

    filepath = find_csv_file(filename)
    questions = load_questions_csv(filepath)

    if not questions:
        print("⚠️ No questions available. Exiting...")
        sys.exit(1)

    print("\n📚 Loaded", len(questions), "questions from dataset.")
    adaptive = input("Enable adaptive difficulty? (y/n): ").strip().lower() == "y"

    score = 0
    num_questions = min(10, len(questions))  # ask up to 10
    start_time = datetime.datetime.now()

    for i in range(num_questions):
        q = random.choice(questions)
        if ask_question(q["q"], q["opts"], q["correct"]):
            score += 1

    end_time = datetime.datetime.now()
    duration = (end_time - start_time).seconds

    print("\n🎉 Quiz Over!")
    print(f"Your final score: {score}/{num_questions}")
    print(f"⏱️ Time taken: {duration} seconds")

if __name__ == "__main__":
    main()