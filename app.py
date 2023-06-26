from flask import Flask, render_template, request

app = Flask(__name__)

habits = ["test habit", 'test habit 2']# this will change to a database after testing


@app.route("/")
def index():
    return render_template("index.html", habits=habits, title="Habit Tracker - Home")


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        # if a post method is recieved get the habit and add it to habits
        habits.append(request.form.get("habit"))
    return render_template("add_habit.html", title="Habit Tracker - Add Habit")

if __name__ == "__main__":
    app.run(debug=True)