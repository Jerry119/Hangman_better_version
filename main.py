from flask import Flask, render_template, request
import random

app = Flask(__name__)


old_guess = ""
word = ""
hint = ""

def setWordHint():
    f = open('word.txt', 'r')
    lines = f.read().split('\n')
    f.close()
    n = random.randint(0, len(lines)-1)
    line = lines[n]
    word = line.split('?')[0]
    hint = line.split('?')[1]
    return word, hint

@app.route('/')
@app.route('/<best_score>')
def home(best_score=0):
    global word
    global hint
    word, hint = setWordHint()
    global old_guess
    old_guess = ""
    return render_template("index.html", word=word, remain_cnt=5, best_score=best_score, hint=hint)

# for unit test purpose
def getHint():
    return hint

# for unit test purpose
def setWord(w):
    global word
    word = w

# for unit test purpose
def setGuess(g):
    global old_guess
    old_guess = g

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


