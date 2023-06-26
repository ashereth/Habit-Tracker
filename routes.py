from flask import Blueprint, render_template, request, redirect, url_for, current_app
import datetime
import uuid
from bson.objectid import ObjectId
from markupsafe import Markup

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")

# function to get the date for 3 days before and 3 days after a given date
# use a context processor so that all templates will have access to the date_range variable
@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        # creates a list of dates from 3 days prior up to 3 days after start date
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day) #by default time is at 0

@pages.route("/")
def index():
    date_str = request.args.get("date")
    # if user clicked on a date the page gets refreshed and selected_date gets set to that date
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    # if the user hasn't clicked on a date then selected_date should be set to today
    else:
        selected_date = today_at_midnight()
    #get all habits that were added on a date less than or equal to current date
    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template(
        "index.html", 
        habits=habits_on_date, 
        completions=completions,
        title="Habit Tracker - Home", 
        selected_date=selected_date
        )


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = today_at_midnight()
    if request.form:
        # if a post method is recieved get the habit and add it to habits
        current_app.db.habits.insert_one({
            "added": today, 
            "name": request.form.get("habit")
            })
    return render_template(
        "add_habit.html", 
        title="Habit Tracker - Add Habit", 
        # selected_date should always be today so that we can only add habits starting from today
        selected_date=today)


#this method will get called whenever someone clicks on an incomplete habit
# and it will add the habit to the completions dictionary
@pages.route("/complete", methods=["POST"])
def complete():
    # get the values for 'date' and 'habitName' from the form
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    #in the completions dictionary at the date element add the habit to the list
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for(".index", date=date_string))

@pages.route("/incomplete", methods=["GET", "POST"])
def incomplete():
    # get the values for 'date' and 'habitName' from the form
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)
    #in the completions dictionary at the date element remove the habit to the list
    current_app.db.completions.delete_one({"date": date, "habit": habit})

    return redirect(url_for(".index", date=date_string))

@pages.route("/remove_habit", methods=["POST"])
def remove_habit():
    date_string = request.form.get("date")
    habit_id = request.form.get("habitId")
    added = request.form.get("added")
    date = datetime.datetime.fromisoformat(date_string)

    current_app.db.habits.delete_one({"_id": habit_id, "added": added, "name": request.form.get("habit")})

    return redirect(url_for(".index", date=date_string))