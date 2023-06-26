from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

habits = ["test habit", 'test habit 2']# this will change to a database after testing

# function to get the date for 3 days before and 3 days after a given date
# use a context processor so that all templates will have access to the date_range variable
@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        # creates a list of dates from 3 days prior up to 3 days after start date
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


@app.route("/")
def index():
    date_str = request.args.get("date")
    # if user clicked on a date the page gets refreshed and selected_date gets set to that date
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    # if the user hasn't clicked on a date then selected_date should be set to today
    else:
        selected_date = datetime.date.today()

    return render_template(
        "index.html", 
        habits=habits, 
        title="Habit Tracker - Home", 
        selected_date=selected_date
        )


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        # if a post method is recieved get the habit and add it to habits
        habits.append(request.form.get("habit"))
    return render_template(
        "add_habit.html", 
        title="Habit Tracker - Add Habit", 
        # selected_date should always be today so that we can only add habits starting from today
        selected_date=datetime.date.today())

if __name__ == "__main__":
    app.run(debug=True)