from flask import Flask, redirect, render_template, request, send_file, url_for
import json
import datetime
import enum
import requests

app=Flask(__name__)

list = []
end_text = "blank"
correct_answer = "drake"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game-started/")
def start_game():
    list.clear()
    return render_template("index.html", game='game.html', list=list)

@app.route("/game-guess/", methods=['POST'])
def game_guess():
    guess = request.form['guess']
    if len(guess) != 5:
        return render_template("index.html", game='game.html', list=list)
    new_guess = [[],[],[],[],[]]
    correct = 0
    for i in range(5):
        if guess[i] == correct_answer[i]:
            correct += 1
            new_guess[i] = [guess[i], "correct"]
        elif guess[i] in correct_answer:
            new_guess[i] = [guess[i], "present"]
        else:
            new_guess[i] = [guess[i], "absent"]
    list.append(new_guess)
    if correct == 5:
        end_text="Congrats! You Won!"
        return redirect(url_for('game_end', ending=end_text))
    elif len(list)>=5:
        end_text="Sorry! You lost!"
        return redirect(url_for('game_end', ending=end_text))
    else:
        return render_template("index.html", game='game.html', list=list)

@app.route("/game-end/")
def game_end():
    ending = request.args['ending']
    return render_template("index.html", game='game.html', list=list, end_text=ending)

if __name__=="__main__":
    app.run(debug=True)
