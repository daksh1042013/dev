from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Game state
score = 0
lives = 5
a = random.randint(1, 9)
b = random.randint(1, 9)

@app.route("/", methods=["GET", "POST"])
def game():
    global score, lives, a, b
    if request.method == "POST":
        try:
            user_answer = int(request.form["product"])
            if user_answer == a * b:
                score += 10
                message = "Correct!"
            else:
                lives -= 1
                message = f"Wrong. The correct answer was {a * b}."

            if lives == 0:
                final_score = score
                score, lives = 0, 5
                a, b = random.randint(1, 9), random.randint(1, 9)
                return render_template("game_over.html", final_score=final_score)

            a, b = random.randint(1, 9), random.randint(1, 9)
        except ValueError:
            message = "Invalid input. Please enter a number."

        return render_template("game.html", score=score, lives=lives, a=a, b=b, message=message)

    return render_template("game.html", score=score, lives=lives, a=a, b=b, message="")

@app.route("/game-over")
def game_over():
    return render_template("game_over.html", final_score=score)

if __name__ == "__main__":
    app.run(debug=True)
