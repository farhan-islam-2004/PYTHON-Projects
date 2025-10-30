## 🧠 Aptitude Quiz Game (Python)

A Python-based terminal quiz application that challenges users with multiple-choice aptitude questions.  
It loads questions from a CSV dataset, shuffles the options, enforces a time limit per question, and displays the final score — all in a clean, cross-platform command-line interface.

---

## 🚀 Features

- 📂 **CSV Question Bank**: Loads questions and answers from a semicolon-separated CSV file.
- 🔀 **Shuffled Options**: Randomizes answer order each time to avoid memorization.
- ⏰ **Time Limit**: Default 30 seconds per question, configurable via `--time-limit`.
- ✅ **Answer Validation**: Checks correctness and shows the right answer if wrong.
- 📊 **Score Summary**: Displays total score and time taken at the end.
- 💻 **Cross-Platform**: Works on Windows, macOS, and Linux with Python 3.

---

## 🧠 Concepts Used

- File Handling with `csv.DictReader`
- Randomization with `random.shuffle`
- Threading for timed input
- Command-line arguments with `argparse`
- Time measurement using `datetime`
- Clean modular code structure

---

## 📊 Dataset Format

The CSV file should use `;` (semicolon) as a delimiter and contain the following columns:

| Column     | Description                          |
|------------|--------------------------------------|
| Question   | The question text                    |
| Option A   | First option                         |
| Option B   | Second option                        |
| Option C   | Third option                         |
| Option D   | Fourth option                        |
| Answer     | Correct answer (A, B, C, or D)       |

---

## 👨‍💻 Author 

- Farhan Islam - B.Tech CSE Student | Aspiring Full Stack Developer 
- LinkedIn Profile - https://www.linkedin.com/in/farhanislam20/ 

--- 
**⭐ Don’t forget to star the repo if you like it!**