from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# רשימת 51 הערכים לבחירה
values = [
    "משפחתיות", "יושרה", "אחריות", "יצירתיות", "אמפתיה", "חברות", "צמיחה אישית", "מנהיגות", "הומור",
    "אומץ", "כנות", "צדק", "כבוד", "עצמאות", "השפעה", "חמלה", "הגינות", "תקשורת", "נאמנות",
    "בריאות", "הערכה", "תכנון קדימה", "הוקרת תודה", "שיתוף פעולה", "מצוינות", "נדיבות", "אמון",
    "איזון", "יציבות", "חדשנות", "למידה", "מקצועיות", "עזרה לזולת", "בטחון עצמי", "שאפתנות",
    "שלווה", "פשטות", "מסורת", "שוויון", "אופטימיות", "סקרנות", "שליטה עצמית", "גמישות", "פתיחות מחשבתית",
    "שמירה על הסביבה", "משמעות", "הגשמה עצמית", "כיף", "רוגע", "משמעת", "התמדה"
]

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        session.clear()  # איפוס כל הנתונים מהעבר
        session["name"] = request.form["name"]
        return redirect(url_for("select_values"))
    return render_template("start.html")

@app.route("/select_values", methods=["GET", "POST"])
def select_values():
    if "selected_values" not in session:
        session["selected_values"] = random.sample(values, 5)
        session["remaining_values"] = list(set(values) - set(session["selected_values"]))
        session["final_selection"] = []

    new_value = session["remaining_values"].pop(0) if session["remaining_values"] else None

    if request.method == "POST":
        action = request.form.get("action")
        selected_value = request.form.get("selected_value")

        if action == "add" and len(session["final_selection"]) < 10 and new_value:
            session["final_selection"].append(new_value)
        elif action == "replace" and selected_value and new_value:
            session["final_selection"].remove(selected_value)
            session["final_selection"].append(new_value)
        elif action == "skip":
            pass  

        session.modified = True
        if len(session["final_selection"]) >= 10 or not session["remaining_values"]:
            return redirect(url_for("rank_values"))

    return render_template("select_values.html", selected_values=session["final_selection"], new_value=new_value)

@app.route("/rank_values", methods=["GET", "POST"])
def rank_values():
    if "final_selection" not in session or len(session["final_selection"]) < 10:
        return redirect(url_for("select_values"))

    if "pairwise_comparisons" not in session or not session["pairwise_comparisons"]:
        session["pairwise_comparisons"] = []
        session["ranking"] = {}

        # יצירת כל זוגות ההשוואה האפשריים
        pairs = [(session["final_selection"][i], session["final_selection"][j]) 
                 for i in range(len(session["final_selection"])) 
                 for j in range(i+1, len(session["final_selection"]))]
        random.shuffle(pairs)  # ערבוב סדר ההשוואות
        session["pairwise_comparisons"] = pairs

    if request.method == "POST":
        winner = request.form.get("winner")
        loser = request.form.get("loser")

        if winner and loser:
            session["ranking"][winner] = session["ranking"].get(winner, 0) + 1
            session["ranking"][loser] = session["ranking"].get(loser, 0)

        if session["pairwise_comparisons"]:
            session["pairwise_comparisons"].pop(0)  # מסירים את הזוג שהושווה

        session.modified = True  # שמירת השינויים

        if not session["pairwise_comparisons"]:  # אם כל ההשוואות הסתיימו, הצג את הסיכום
            sorted_ranking = sorted(session["ranking"].items(), key=lambda x: x[1], reverse=True)
            session["ranked_selection"] = [item[0] for item in sorted_ranking]
            return redirect(url_for("summary"))

    if session["pairwise_comparisons"]:
        pair = session["pairwise_comparisons"][0]
        return render_template("rank_values.html", option1=pair[0], option2=pair[1])

    return redirect(url_for("summary"))

@app.route("/summary")
def summary():
    if "ranked_selection" not in session:
        return redirect(url_for("select_values"))

    return render_template("summary.html", name=session["name"], ranked_selection=session["ranked_selection"])

# תמיכה ב-PWA
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
