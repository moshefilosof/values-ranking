
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# כותרת המערכת
st.title("🔍 ניתוח התשובות שלך - תובנות מותאמות אישית")

# פונקציה לניתוח התשובות ולמיפוי הצרכים, הסגנון הרגשי וחוק היקום
def analyze_responses(responses):
    results = {"need": "", "emotional_style": "", "universal_law": ""}

    # ניתוח הצורך הבסיסי
    if "דג מחוץ למים" in responses or "חיפוש חום ואישור" in responses:
        results["need"] = "שייכות - חוסר תחושת חיבור אמיתי"
    elif "מטפס הרים" in responses or "משהו מחזיר אותי אחורה" in responses:
        results["need"] = "מסוגלות - פחד מהתקדמות ואי הצלחה"
    else:
        results["need"] = "עצמאות - קושי בקבלת החלטות לבד"

    # ניתוח הסגנון הרגשי
    if "מחסום ללא מוצא" in responses or "אני חוזר שוב ושוב" in responses:
        results["emotional_style"] = "חוסן רגשי נמוך - תחושת תקיעות"
    elif "קפטן של ספינה" in responses or "משהו תמיד מחזיר אותי אחורה" in responses:
        results["emotional_style"] = "רגישות להקשר - ניתוח יתר של הסביבה"
    else:
        results["emotional_style"] = "אינטואיציה חברתית - צורך בהכרה חיצונית"

    # ניתוח חוק היקום הלא ממומש
    if "אני נותן הרבה אבל לא מקבל חזרה" in responses:
        results["universal_law"] = "חוק הפיצוי - צורך ללמוד קבלה"
    elif "הדברים שאני הכי רוצה מתרחקים ממני" in responses:
        results["universal_law"] = "חוק המשיכה - צורך לשנות תדרים פנימיים"
    else:
        results["universal_law"] = "חוק הסיבה והתוצאה - דפוסי פעולה שחוזרים על עצמם"

    return results

# טופס למילוי התשובות
st.subheader("📋 הזן את תשובותיך מהשאלון")
q1 = st.text_input("תשובתך למסע החיים")
q2 = st.text_input("תשובתך לתחושות הגוף")
q3 = st.text_input("תשובתך לדימוי האישי")
q4 = st.text_input("תשובתך לחוק היקום")

if st.button("🔍 נתח את התשובות שלי"):
    responses = [q1, q2, q3, q4]
    results = analyze_responses(responses)

    # הצגת תובנות
    st.subheader("✨ התובנות האישיות שלך")
    st.write(f"🔹 **הצורך הלא מאוזן:** {results['need']}")
    st.write(f"🔹 **הסגנון הרגשי שהתעצב:** {results['emotional_style']}")
    st.write(f"🔹 **חוק היקום שלא ממומש:** {results['universal_law']}")

    # יצירת גרף ויזואלי
    labels = ["שייכות", "עצמאות", "מסוגלות"]
    values = [1 if "שייכות" in results["need"] else 0, 
              1 if "עצמאות" in results["need"] else 0, 
              1 if "מסוגלות" in results["need"] else 0]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'green', 'red'])
    ax.set_ylabel("רמת חוסר איזון")
    ax.set_title("ניתוח הצרכים שלך")
    st.pyplot(fig)
