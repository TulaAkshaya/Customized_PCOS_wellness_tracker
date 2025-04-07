import streamlit as st
import pandas as pd
import datetime
import urllib.parse

# --- App Config ---
st.set_page_config(page_title="PCOS Wellness Tracker", layout="centered")
st.title(" PCOS Daily Glow-Up Tracker")

# --- Date & Init ---
today = datetime.date.today()
st.markdown(f"#### 📅 {today.strftime('%A, %B %d, %Y')}")

if 'completed_days' not in st.session_state:
    st.session_state.completed_days = {}
if 'mood_log' not in st.session_state:
    st.session_state.mood_log = {}

# --- Daily Habits ---
st.markdown("### ✅ Daily Habits")

habits = {
    "Drink spearmint tea": "10:00",
    "Eat 1–2 tbsp flax seeds": "08:30",
    "30 mins walk/yoga": "17:00",
    "2L+ water": None,
    "Sleep 7+ hours": "22:30",
    "Magnesium or Inositol supplement": "21:00",
    "Gentle skincare routine": "20:30",
    "Journaling or breathwork": "21:30"
}

completed = []
for habit, time_str in habits.items():
    checked = st.checkbox(habit)
    if checked:
        completed.append(habit)
    else:
        st.warning(f"⏰ Don’t forget to: **{habit}** — You got this! 💪")

    # Google Calendar link
    if time_str:
        start_time = datetime.datetime.combine(today, datetime.datetime.strptime(time_str, "%H:%M").time())
        end_time = start_time + datetime.timedelta(minutes=15)
        start_str = start_time.strftime("%Y%m%dT%H%M00Z")
        end_str = end_time.strftime("%Y%m%dT%H%M00Z")
        event_url = (
            f"https://calendar.google.com/calendar/r/eventedit?"
            f"text={urllib.parse.quote(habit)}"
            f"&dates={start_str}/{end_str}"
            f"&details=Gentle+PCOS+Reminder"
        )
        st.markdown(f"[📆 Add to Google Calendar]({event_url})")

# Save today's completion
st.session_state.completed_days[str(today)] = len(completed)
st.success(f"You’ve completed {len(completed)} out of {len(habits)} habits today! 💪")

# --- Mood Tracker ---
st.markdown("### 🫶 How are you feeling today?")
mood = st.radio("Select your mood:", ["😊 Happy", "😐 Neutral", "😔 Low"], key=str(today))
st.session_state.mood_log[str(today)] = mood

# --- Encouraging Tips Based on Mood ---
st.markdown("### Encouraging Tip of the Day")
if mood == "😊 Happy":
    st.success("You’re glowing! Keep up the amazing work and remember to celebrate the small wins ✨")
elif mood == "😐 Neutral":
    st.info("You’re doing your best and that’s enough today. Maybe a walk or warm tea will lift your vibe ☁️💗")
elif mood == "😔 Low":
    st.warning("It’s okay to feel this way. Be gentle with yourself. You are healing — one step at a time 🫶")

# --- Weekly Progress Tracker ---
st.markdown("---")
st.markdown("### 📊 Weekly Progress Tracker")

week_dates = [today - datetime.timedelta(days=(today.weekday() - i) % 7) for i in range(7)]
week_dates.sort()
day_labels = [date.strftime('%A (%d %b)') for date in week_dates]
progress_data = [
    st.session_state.completed_days.get(str(date), 0)
    for date in week_dates
]

# Create DataFrame for bar chart
df = pd.DataFrame({"Day": day_labels, "Habits Done": progress_data})
st.bar_chart(df.set_index("Day"))

# --- Tips Section ---
st.markdown("---")
st.markdown("### 💡 Natural Tips for PCOS")
st.info("✅ Rinse your scalp weekly with diluted apple cider vinegar to reduce itch + oil.")
st.info("✅ Try cinnamon or fenugreek water in the morning to support blood sugar.")
st.info("✅ Keep a sleep routine — hormones love consistency!")

# --- iOS Instructions ---
st.markdown("---")
st.markdown("### 📱 Tip: Add This App to Your iPhone Home Screen")
st.markdown("1. Open this app in Safari.\n2. Tap the 'Share' icon.\n3. Select 'Add to Home Screen'.")
st.caption("Now it works just like a native app! 💖")

# --- Footer ---
st.markdown("---")
st.markdown("Made with 💕 for PCOS warriors ✨")
