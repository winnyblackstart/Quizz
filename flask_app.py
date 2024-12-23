
from flask import Flask, render_template, request, redirect, url_for, session
import random
import copy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    {"question": "What is the output of the following code: print(2 ** 3)?", "options": ["6", "8", "9", "16"], "answer": "8"},
    {"question": "Which of the following is used to define a function in Python?", "options": ["def", "function", "func", "define"], "answer": "def"},
    {"question": "What will the following code print: print('Python'[::-1])?", "options": ["nohtyP", "Python", "TypeError", "SyntaxError"], "answer": "nohtyP"},
    {"question": "Which method is used to add an element to the end of a list in Python?", "options": ["add()", "append()", "insert()", "extend()"], "answer": "append()"},
    {"question": "What is the correct syntax for importing the math module in Python?", "options": ["import math", "import math()", "from math import *", "include math"], "answer": "import math"},
    {"question": "How do you declare a variable in Python?", "options": ["var x = 10", "x = 10", "let x = 10", "declare x = 10"], "answer": "x = 10"},
    {"question": "Which of the following is a mutable data type in Python?", "options": ["list", "string", "tuple", "int"], "answer": "list"},
    {"question": "What will be the output of the following code: print(10 // 3)?", "options": ["3", "3.33", "10", "Error"], "answer": "3"},
    {"question": "How do you write a comment in Python?", "options": ["// comment", "/* comment */", "# comment", "/* comment"], "answer": "# comment"},
    {"question": "What does the 'break' statement do in a loop?", "options": ["Terminates the loop", "Skips the current iteration", "Pauses the loop", "None of the above"], "answer": "Terminates the loop"}
]
Questions = copy.deepcopy(questions)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['totalQuestions'] = 4
        session['questions'] = questions
        session['Questions'] = Questions
        session['current_question'] = int(random.random() * len(questions))-1
        session['answers'] = []
        session ['index'] = []
        session['answered'] = 0
        return redirect(url_for('questionnaire'))
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if 'current_question' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'skip' in request.form:
            session['answers'].append(None)
            
        else:
            session['answers'].append(request.form['answer'])
            for i in range (len(session ['Questions'])):
            	if session['Questions'][i] == session['questions'][session['current_question']]:
            		session['index'].append(i)
            session['questions'].pop(session['current_question'])
            session ['answered'] += 1

        session['current_question'] = random.randint(0, len(session ['questions']))-1

        if session['answered'] >= session['totalQuestions']:
            return redirect(url_for('result'))

    current_question = session['questions'][session['current_question']]
    return render_template('questionnaire.html', question=current_question)

@app.route('/result')
def result():
    name = session['name']
    answers = session['answers']  # Dictionary containing answers with question indices as keys
    index = session['index']  # List of indices corresponding to the questions answered
    Questions = session['Questions']
    totalQuestions = session['totalQuestions']
    score = 0

    print('MyAnswers:', answers, 'Indices:', index)

    # Iterate over the indices to match answers with the corresponding questions
    for i in index:
        for j, answer in enumerate(answers):
            print(f"Correct Answer for Question {i}: {Questions[i]['answer']}")
            if answers[j] == Questions[i]['answer']:  # Check if the answer matches
                score += 1

    # Calculate the percentage score
    percentage = round((score / totalQuestions) * 100, 1)
    color = get_color(percentage)

    return render_template('result.html', name=name, score=percentage, color=color)

def get_color(percentage):
    if percentage >= 90:
        return 'goldenrod'
    elif percentage >= 60:
        return 'green'
    elif percentage >= 40:
        return 'darkorange'
    else:
        return 'darkred'

if __name__ == '__main__':
    app.run(debug=True)
    