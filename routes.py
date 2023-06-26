from flask import Blueprint, render_template, request, redirect, url_for
import datetime
from collections import defaultdict

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")

habits = ["test habit", 'test habit 2']# this will change to a database after testing
# makes a dictionary mapping things to lists  ex:  {"2022-02-13": ["test habit"]} 
# if a key value doesn't exist it automatically makes it and maps it to a list
completions = defaultdict(list)


# function to get the date for 3 days before and 3 days after a given date
# use a context processor so that all templates will have access to the date_range variable
@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        # creates a list of dates from 3 days prior up to 3 days after start date
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


@pages.route("/")
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
        completions=completions[selected_date],
        title="Habit Tracker - Home", 
        selected_date=selected_date
        )


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        # if a post method is recieved get the habit and add it to habits
        habits.append(request.form.get("habit"))
    return render_template(
        "add_habit.html", 
        title="Habit Tracker - Add Habit", 
        # selected_date should always be today so that we can only add habits starting from today
        selected_date=datetime.date.today())


#this method will get called whenever someone clicks on an incomplete habit
# and it will add the habit to the completions dictionary
@pages.route("/complete", methods=["POST"])
def complete():
    # get the values for 'date' and 'habitName' from the form
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    #in the completions dictionary at the date element add the habit to the list
    completions[date].append(habit)

    return redirect(url_for(".index", date=date_string))

@pages.route("/incomplete", methods=["POST"])
def incomplete():
    # get the values for 'date' and 'habitName' from the form
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    #in the completions dictionary at the date element remove the habit to the list
    completions[date].remove(habit)

    return redirect(url_for(".index", date=date_string))
