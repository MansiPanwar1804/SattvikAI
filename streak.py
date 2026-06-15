import json
from datetime import date, timedelta, datetime

FILE = "streak_data.json"

def load_streak():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "current": 0,
            "longest": 0,
            "last_date": None,
            "history": []  # every successful day logged here
        }

def save_streak(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def update_streak():
    data = load_streak()
    today = str(date.today())

    # If already counted today — do nothing
    if data["last_date"] == today:
        return data

    yesterday = str(date.today() - timedelta(days=1))

    # Continue streak
    if data["last_date"] == yesterday:
        data["current"] += 1
    else:
        data["current"] = 1  # streak restart

    # Update stats
    data["last_date"] = today
    data["longest"] = max(data["longest"], data["current"])

    # Add to history if new day
    if today not in data["history"]:
        data["history"].append(today)

    save_streak(data)
    return data


# ---------- Calendar Generator ----------
def get_month_calendar():
    today = date.today()
    first = today.replace(day=1)
    month = today.month
    year = today.year

    history = load_streak()["history"]

    days = []
    day = first
    while day.month == month:
        day_str = str(day)
        days.append({
            "date": day_str,
            "completed": day_str in history
        })
        day += timedelta(days=1)

    return days


# ---------- Badge System ----------
def get_badges(current):
    badges = []

    if current >= 7:
        badges.append("🔥 7-Day Streak Achieved!")

    if current >= 14:
        badges.append("⭐ 14-Day Warrior!")

    if current >= 30:
        badges.append("🏆 30-Day Champion!")

    return badges
