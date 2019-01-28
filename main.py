from flask import Flask, render_template, request
import random

app = Flask(__name__)

word = ""
hint = ""
old_guess = ""

@app.route('/')
@app.route('/<best_score>')
def home(best_score=0):
    f = open('word.txt', 'r')
    lines = f.read().split('\n')
    n = random.randint(0, len(lines)-1)
    line = lines[n]
    global word
    word = line.split('?')[0]
    global hint
    hint = line.split('?')[1]
    global old_guess
    old_guess = ""
    f.close()

    return render_template("index.html", word=word, remain_cnt=5, best_score=best_score, hint=hint)

@app.route('/in_game', methods=["POST"])
def in_game():
    remain_cnt = int(request.form['remain_cnt'])
    char = request.form['char'].lower()
    best_score = int(request.form['best_score'])
    
    global old_guess
    
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

        old_guess = new_guess

        if '_' not in new_guess:
            if remain_cnt > best_score:
                best_score = remain_cnt
            return render_template("win.html", word=word, remain_cnt=remain_cnt, best_score=best_score, hint=hint)
    else:
        remain_cnt -= 1
        if remain_cnt == 0:
            return render_template("fail.html", word=word, remain_cnt=remain_cnt, best_score=best_score, hint=hint)
    
    return render_template("playing.html", remain_cnt=remain_cnt, guess=old_guess, best_score=best_score, hint=hint)


