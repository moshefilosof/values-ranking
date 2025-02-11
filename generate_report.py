import streamlit as st
import pandas as pd
from datetime import datetime
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# הוראות התקנה והרצה:
# 1. ודא שפייתון מותקן במחשב.
# 2. התקן את Streamlit והרצות הדרושות:
#    pip install streamlit pandas reportlab
# 3. שמור קובץ זה בשם "values_needs_app.py" בתיקיית myapp.
# 4. להפעלת היישום, פתח שורת פקודה ונווט לתיקייה myapp:
#    cd C:\Users\המשתמש\myapp
# 5. הפעל את היישום עם הפקודה:
#    streamlit run values_needs_app.py

# הגדרת רשימת 51 הערכים האפשריים
values = [
    "עצמאות", "חמלה", "בטיחות", "עקביות", "חריצות", "בריאות", "פשטות", "יוזמה", "גמישות",
    "פרטיות", "יושרה", "דאגה לסביבה", "פתיחות", "יצירתיות", "דייקנות", "צדק", "כבוד", "דימוי עצמי",
    "אמפתיה", "כיף", "הגינות", "רוגע", "כנות", "הוקרה", "שוויון", "כסף ורכוש", "החלטיות", "שימור המסורת",
    "מחילה", "הערכה", "שיתוף פעולה", "מנהיגות", "השפעה", "שליטה עצמית", "מעשיות", "התמדה", "שמחה",
    "משפחתיות", "חברות", "תכנון", "נאמנות", "חדשנות", "תמיכה", "נדיבות", "חיבה", "תקשורת", "סבלנות",
    "אופטימיות", "תרומה", "סדר", "חיסכון"
]

# ערבוב רשימת הערכים
random.shuffle(values)

# משתני מצב
if 'selected_values' not in st.session_state:
    st.session_state.selected_values = values[:5]
    st.session_state.remaining_values = values[5:]
    st.session_state.final_values = []
    st.session_state.step = 1

st.title("שאלון זיהוי ערכים וצרכים")

# שלב בחירת 10 הערכים
if st.session_state.step == 1:
    st.subheader("בחר את הערכים החשובים לך ביותר")
    
    new_value = None
    if st.session_state.remaining_values:
        new_value = st.session_state.remaining_values.pop(0)
        st.write(f"**ערך חדש:** {new_value}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❌ דלג על הערך"):
            st.session_state.final_values.append(None)
    with col2:
        if len(st.session_state.selected_values) < 10 and st.button("✅ הוסף לרשימה"):
            st.session_state.selected_values.append(new_value)
    with col3:
        if st.session_state.selected_values and st.button("🔄 החלף ערך קיים"):
            removed_value = st.selectbox("בחר ערך להחלפה:", st.session_state.selected_values)
            st.session_state.selected_values.remove(removed_value)
            st.session_state.selected_values.append(new_value)
    
    st.write("**הערכים שנבחרו עד כה:**", st.session_state.selected_values)
    
    if len(st.session_state.selected_values) == 10 or not st.session_state.remaining_values:
        st.session_state.step = 2
        st.experimental_rerun()

# שלב דירוג 10 הערכים
if st.session_state.step == 2:
    st.subheader("דרג את 10 הערכים שנבחרו מהחשוב ביותר (1) לפחות חשוב (10)")
    ranked_values = {}
    
    for value in st.session_state.selected_values:
        ranked_values[value] = st.slider(f"דרג את {value}", 1, 10, 5)
    
    if st.button("המשך לניתוח הצרכים"):
        st.session_state.ranked_values = dict(sorted(ranked_values.items(), key=lambda item: item[1]))
        st.session_state.step = 3
        st.experimental_rerun()

# שלב ניתוח הצרכים הבסיסיים
if st.session_state.step == 3:
    st.subheader("ניתוח התאמה לצרכים הבסיסיים")
    needs_mapping = {
        "שייכות": ["משפחתיות", "שיתוף פעולה", "חברות", "תמיכה", "אמפתיה", "נדיבות", "חיבה", "תקשורת", "כיף"],
        "עצמאות": ["עצמאות", "שליטה עצמית", "יוזמה", "חדשנות", "מנהיגות", "כנות", "תכנון", "פרטיות", "חמלה"],
        "מסוגלות": ["התמדה", "החלטיות", "דייקנות", "בריאות", "חריצות", "מעשיות", "השפעה", "פתיחות", "יצירתיות"]
    }
    need_scores = {"שייכות": 0, "עצמאות": 0, "מסוגלות": 0}
    
    for value in st.session_state.selected_values:
        for need, related_values in needs_mapping.items():
            if value in related_values:
                need_scores[need] += 1
    
    st.write(pd.DataFrame.from_dict(need_scores, orient="index", columns=["מספר ערכים מתאימים"]))
    st.success("תהליך זיהוי הערכים והצרכים הושלם!")
