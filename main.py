from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
@app.route('/<best_score>')
def home(best_score=0):
    f = open('word.txt', 'r')
    lines = f.read().split('\n')
    n = random.randint(0, len(lines)-1)
    line = lines[n]
    word = line.split('?')[0]
    hint = line.split('?')[1]
    f.close()

    return render_template("index.html", word=word, remain_cnt=5, best_score=best_score, hint=hint)

@app.route('/in_game', methods=["POST"])
def in_game():
    remain_cnt = int(request.form['remain_cnt'])
    char = request.form['char'].lower()
    word = request.form['word']
    old_guess = request.form['guess']
    best_score = int(request.form['best_score'])
    hint = request.form['hint']
    
    if old_guess == "":
        for c in word:
            if c == ' ':
                old_guess += c
            else:
                old_guess += '_'
    
    if char in word.lower():
        new_guess = ""
        for i in range(len(word)):
            if word[i].lower() == char:
                new_guess += word[i]
            else:
                new_guess += old_guess[i]

        if '_' not in new_guess:
            if remain_cnt > best_score:
                best_score = remain_cnt
            return render_template("win.html", word=word, remain_cnt=remain_cnt, best_score=best_score, hint=hint)
    else:
        new_guess = old_guess
        remain_cnt -= 1
        if remain_cnt == 0:
            return render_template("fail.html", word=word, remain_cnt=remain_cnt, best_score=best_score, hint=hint)
    
    return render_template("playing.html", remain_cnt=remain_cnt, word=word, guess=new_guess, best_score=best_score, hint=hint)


