from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

QUESTIONS_DIR = "questions"

def get_topics():
    return [f.replace(".json", "") for f in os.listdir(QUESTIONS_DIR) if f.endswith(".json")]

def load_questions(topic):
    filepath = os.path.join(QUESTIONS_DIR, f"{topic}.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template("index.html", topics=get_topics())

@app.route('/quiz/<topic>/<int:q>', methods=['GET', 'POST'])
def quiz_topic(topic, q):
    questions = load_questions(topic)

    if q >= len(questions):
        return render_template("finished.html", topic=topic)

    question = questions[q]
    result = None

    if request.method == 'POST':
        user_answer = request.form['answer']
        correct = question['answer']
        result = "✅ Правильно!" if user_answer == correct else f"❌ Неправильно. Правильный ответ: {correct}"

    return render_template("quiz.html",
                           question=question,
                           result=result,
                           num=q,
                           total=len(questions),
                           topic=topic)

if __name__ == '__main__':
    app.run(debug=True)