from flask import Flask

app = Flask(__name__)

# עמוד הבית - בדיקה שהשרת עובד
@app.route("/")
def home():
    return "Flask פועל בהצלחה ב-Railway!"

# דף נוסף לבדיקה
@app.route("/test")
def test():
    return "בדיקת Route נוסף ב-Railway!"

# הרצת האפליקציה עם ההגדרות הנכונות
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
