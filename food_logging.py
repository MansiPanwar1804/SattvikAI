# food_logging.py — Premium Clean UI for SattvikAI
import streamlit as st
import matplotlib.pyplot as plt
import base64
from ai_analysis import generate_ai_analysis
from streak import update_streak, get_month_calendar, get_badges
from datetime import datetime
import calendar as cal


# ---------- LOAD BACKGROUND IMAGE ----------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------- LOAD LOGO ----------
def load_logo(image_file, width=90):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    return f'<img src="data:image/png;base64,{encoded}" width="{width}">'


# ----------------------------------------------------------------
# MAIN APP FUNCTION
# ----------------------------------------------------------------
def run_food_logging():
    st.set_page_config(page_title="SattvikAI | Food Tracker", layout="centered")

    # Hide Streamlit UI elements
    st.markdown("""
        <style>
        header {visibility: hidden;}
        .stApp > header {display: none;}
        .st-emotion-cache-18ni7ap {display: none;}
        .st-emotion-cache-h5rgaw {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # Background + Logo
    add_bg_from_local("assets/bg.png")
    logo_html = load_logo("assets/plate.png", width=110)

    # HEADER
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:20px;">
            {logo_html}
            <h1 style='color:#1f5131; margin-bottom:0;'>SattvikAI</h1>
            <h3 style='color:#3b7049; margin-top:4px;'>Food Tracker | Today’s Summary</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # INPUTS
    meals = st.text_input("🍱 Meals", placeholder="e.g., 2 roti, dal, sabji")
    water = st.text_input("💧 Water Intake", placeholder="e.g., 6 glasses")
    snacks = st.text_input("🍪 Snacks", placeholder="e.g., peanuts, chips")

    # BUTTON
    if st.button("Analyze My Day"):

        # AI OUTPUT
        with st.spinner("Analyzing with SattvikAI..."):
            data = generate_ai_analysis(meals, water, snacks)

        # UPDATE STREAK
        streak = update_streak()
        calendar_data = get_month_calendar()
        badges = get_badges(streak["current"])

        # STATUS + MACROS
        status = data.get("status", "Balanced")
        macros = data.get("visual_data", {"carbs": 55, "protein": 20, "fat": 25})
        carbs, protein, fat = float(macros["carbs"]), float(macros["protein"]), float(macros["fat"])

        # PIE CHART
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie([carbs, protein, fat],
               labels=["Carbs", "Protein", "Fat"],
               autopct='%1.0f%%',
               startangle=90,
               colors=["#FFA500", "#32CD32", "#1E90FF"],
               textprops={'fontsize': 12})
        ax.set(aspect='equal')
        ax.set_title(status, fontsize=18, weight='bold')
        st.pyplot(fig)

        # SUMMARY
        st.markdown(
            f"<h3 style='text-align:center; color:#2E5E3E;'>Your today's intake is <b>{status}</b> — "
            f"Carbs: {carbs}% | Protein: {protein}% | Fat: {fat}%</h3>",
            unsafe_allow_html=True
        )
        st.markdown("<hr>", unsafe_allow_html=True)

        # STREAK BOX
        st.markdown(f"""
            <div style='background:#FFF4DB; padding:15px;
            border-radius:12px; margin-top:15px;
            box-shadow:0 4px 12px rgba(0,0,0,0.1);'>
                <h3 style='margin:0; color:#D35400;'>🔥 Streak: {streak["current"]} days</h3>
                <p style='margin:0; color:#A04000;'>🏆 Longest: {streak["longest"]} days</p>
            </div>
        """, unsafe_allow_html=True)

        # BADGES
        if badges:
            st.markdown("<h4 style='color:#1f5131; margin-top:15px;'>Achievements</h4>",
                        unsafe_allow_html=True)
            for b in badges:
                st.markdown(
                    f"<div style='padding:10px; background:#E8F8F5; border-radius:10px; "
                    f"margin:5px 0; color:#0a6b4f;'>{b}</div>",
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------------------
        # REAL MONTH CALENDAR (NO CODE BREAKING)
        # ----------------------------------------------------------------
        now = datetime.now()
        year, month, today = now.year, now.month, now.day

        # Month title
        st.markdown(
            f"<h4 style='color:#1f5131; margin-top:25px;'>📅 {now.strftime('%B %Y')}</h4>",
            unsafe_allow_html=True
        )

        # Weekday row
        weekday_html = "<div style='display:flex; gap:10px; margin-bottom:10px;'>"
        for d in ["M", "T", "W", "T", "F", "S", "S"]:
            weekday_html += f"<div style='width:32px;text-align:center;color:#444;font-weight:bold;'>{d}</div>"
        weekday_html += "</div>"
        st.markdown(weekday_html, unsafe_allow_html=True)

        # Month grid
        cal_obj = cal.Calendar(firstweekday=0)
        month_matrix = cal_obj.monthdayscalendar(year, month)

        html = "<div style='display:flex; flex-direction:column; gap:8px;'>"

        for week in month_matrix:
            row = "<div style='display:flex; gap:10px;'>"
            for day in week:

                if day == 0:
                    row += "<div style='width:32px;height:32px;'></div>"
                    continue

                completed = calendar_data[day - 1]["completed"]

                if completed:
                    # Golden streak
                    row += (
                        f"<div style='width:32px;height:32px;border-radius:50%;"
                        f"background:#f4d803;color:#000;display:flex;align-items:center;"
                        f"justify-content:center;font-weight:bold;box-shadow:0 0 8px gold;'>{day}</div>"
                    )
                elif day == today:
                    # Today highlight
                    row += (
                        f"<div style='width:32px;height:32px;border-radius:50%;"
                        f"background:#fff4cc;color:#b88600;display:flex;align-items:center;"
                        f"justify-content:center;font-weight:bold;box-shadow:0 0 8px #ffdd66;'>{day}</div>"
                    )
                else:
                    # Normal day
                    row += (
                        f"<div style='width:32px;height:32px;border-radius:50%;"
                        f"background:#efefef;color:#777;display:flex;align-items:center;"
                        f"justify-content:center;'>{day}</div>"
                    )

            row += "</div>"
            html += row

        html += "</div>"

        # Render final calendar
        st.markdown(html, unsafe_allow_html=True)

        # ----------------------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------------------
        recs = data.get("recommendations", [])

        st.markdown("<h3 style='color:#2E5E3E; margin-top:30px;'>SattvikAI Insights</h3>",
                    unsafe_allow_html=True)

        if recs:
            st.markdown(
                "<div style='background:#F6F9F4; padding:15px; border-radius:10px;'>"
                "<h4 style='margin-top:0; color:#1f5131;'>Recommendations</h4>"
                "</div>", unsafe_allow_html=True)
            for r in recs:
                st.markdown(f"<li style='margin:6px 0; color:#2E5E3E;'>{r}</li>",
                            unsafe_allow_html=True)
        else:
            st.info("No recommendations returned.")

        # ----------------------------------------------------------------
        # REWARD / NOTE
        # ----------------------------------------------------------------
        if status == "Balanced":
            reward = data.get("reward", "Great job today!")
            st.markdown(
                f"""
                <div style='background:#E8F8F5; padding:15px;
                border-radius:10px; margin-top:10px;'>
                    <h4 style='margin-top:0; color:#0a6b4f;'>Reward</h4>
                    <p style='color:#0a6b4f;'>{reward}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if status == "Under Consumed":
                msg = "Your intake was low today — try increasing nutritious foods and proper meals."
                bg = "#FEF9E7"; color = "#7D6608"
            else:
                msg = "You've consumed more than needed — try reducing oily/processed food next time."
                bg = "#FDEDEC"; color = "#922B21"

            st.markdown(
                f"""
                <div style='background:{bg}; padding:15px;
                border-radius:10px; margin-top:10px;'>
                    <h4 style='margin-top:0; color:{color};'>Note</h4>
                    <p style='color:{color};'>{msg}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# RUN APP
if __name__ == "__main__":
    run_food_logging()
