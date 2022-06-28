from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import random
from bson.objectid import ObjectId

app = Flask("JumbledWords")
app.config['MONGO_URI'] = "mongodb://localhost:27017/JumbledWords-db"

Bootstrap(app)

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def word_jumbler():
    if request.method == 'GET':

        return render_template('JumbledWords.html')

@app.route('/jumble', methods=['GET', 'POST'])
def jumbler():
    if request.method == 'GET':
        return render_template('JumbleAWord.html')
    elif request.method == 'POST':
        doc = {'word': request.form['word'].strip().upper()}
        print(doc)
        mongo.db.words.insert_one(doc)
        return redirect('/')
@app.route('/figureout', methods=['GET', 'POST'])
def figureout():
    found_docs = list(mongo.db.words.find())
    total_words = len(found_docs)
    if total_words == 0:
        return redirect('/')
    if request.method == 'GET':
        for doc in found_docs:
            jumbled_word_letters = list(doc['word'])
            random.shuffle(jumbled_word_letters)
            jumbled_word = ''.join(jumbled_word_letters)
            doc['word'] = jumbled_word
        print(total_words)
        return render_template('find-the-words.html', docs=found_docs, count=total_words)
    elif request.method == 'POST':
        score = 0
        user_answers = []
        a = request.form.to_dict(flat=False)['answer']
        print(a)
        for item in a:
            user_answers.append(item.strip().upper())
        print(user_answers,found_docs)
        for index in range(0, total_words, 1):
            if user_answers[index] == found_docs[index]['word']:
                score+=1
        percent = score/total_words * 100
        grade=''
        message = ''
        if 90<= percent<100:
            grade='A'
            message = 'Excellent!'
        elif 80<= percent<90:
            grade='B'
            message = 'Good Job! '
        elif 70<= percent<80:
            grade='C'
            message = 'You did okay.'
        elif 60<= percent<70:
            grade='D'
            message = 'You almost passed. Try again.'
        elif 0<= percent<60:
            grade='F'
            message = 'You failed. Try again.'
        elif percent == 100:
            grade= 'X'
            message = 'YOU GOT A PERFECT SCORE!'

        print(grade, percent)
        return render_template('results.html', score=str(score), count=total_words, grade=grade, message=message)
@app.route('/clear')
def clear():
    mongo.db.words.drop()

    return redirect('/')


app.run(debug=True)
