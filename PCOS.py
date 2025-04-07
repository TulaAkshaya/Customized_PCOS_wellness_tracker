import streamlit as st
import pandas as pd
import datetime
import urllib.parse
import os
import random
import webbrowser

# --- App Config ---
st.set_page_config(page_title="PCOS Wellness Tracker", layout="centered")
st.title("✨ PCOS Daily Glow-Up Tracker")

# --- Morning Reminder ---
current_time = datetime.datetime.now().time()
if current_time < datetime.time(12, 0):
    st.markdown("### 🌞 Good Morning!")
    st.success("This morning is a fresh start. You are capable, you are healing, and your glow-up is unstoppable. ✨✨")


# --- Date & Init ---
today = datetime.date.today()
st.markdown(f"#### 🗕️ {today.strftime('%A, %B %d, %Y')}")

# --- Load or Init Data ---
data_file = "data.csv"
if os.path.exists(data_file):
    df_all = pd.read_csv(data_file)
else:
    df_all = pd.DataFrame(columns=["date", "completed_habits", "mood"])

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
        st.markdown(f"[🗖️ Add to Google Calendar]({event_url})")

# --- Mood Tracker ---
st.markdown("### ✨ How are you feeling today? ✨")
mood = st.radio("Select your mood:", ["😊 Happy", "😐 Neutral", "😔 Low"], key=str(today))

# --- Save to file ---
existing_row = df_all[df_all["date"] == str(today)]
if existing_row.empty:
    new_row = pd.DataFrame({
        "date": [str(today)],
        "completed_habits": [len(completed)],
        "mood": [mood]
    })
    df_all = pd.concat([df_all, new_row], ignore_index=True)
    df_all.to_csv(data_file, index=False)

# --- Daily Completion Feedback ---
st.success(f"You’ve completed {len(completed)} out of {len(habits)} habits today! 💪")

# --- Daily Love Note Based on Mood ---
st.markdown("### ✨✨ Gentle Reminder ✨✨")

mood_notes = {
    "😊 Happy": [
        "You are radiating joy — don’t forget to soak it in! ✨",
        "Your smile is magic — thank you for sharing it with the world. 🌟",
        "Celebrate this glow! You’re doing amazing. ",
        "Keep shining — happiness looks beautiful on you. ☀️",
        "You’re on the right path, and it shows! 💫",
        "Every joyful breath is a gift — enjoy it fully. ",
        "You're unstoppable when your heart is light. 💃"
    ],
    "😐 Neutral": [
        "Even on ‘meh’ days, your presence matters. 💗",
        "Gentle reminder: slow is still progress. 🌱",
        "You’re allowed to just *be* — no pressure, just peace. ☁️",
        "You’re steady, you’re trying — and that’s beautiful. 💖",
        "Today doesn’t have to be perfect to be worth something. ",
        "Breathe deep. You're safe here. 🌿",
        "Balance isn’t boring — it’s powerful. ⚖️"
    ],
    "😔 Low": [
        "You’re not alone. This feeling will pass.",
        "Be soft with yourself today. You’re still healing. 💜",
        "You don’t have to be strong all the time. Just breathe. 🫲",
        "Even broken hearts keep beating. You’re doing beautifully. ❤️",
        "Rest is not weakness. It’s sacred.",
        "You’re allowed to cry. You’re allowed to fall apart. Still, you’re worthy. ",
    ]
}

weekday_idx = today.weekday()
selected_note = mood_notes.get(mood, ["You are enough."])[weekday_idx % 7]
st.success(selected_note)

# --- Encouraging Tips Based on Mood ---
st.markdown("###  Encouraging Tip of the Day")
if mood == "😊 Happy":
    st.success("You’re glowing! Keep up the amazing work and remember to celebrate the small wins ✨")
elif mood == "😐 Neutral":
    st.info("You’re doing your best and that’s enough today. Maybe a walk or warm tea will lift your vibe 💗")
elif mood == "😔 Low":
    st.warning("It’s okay to feel this way. Be gentle with yourself. You are healing — one step at a time ")

# --- Mood-Based Random Spotify Music ---
st.markdown("### 🎵 Mood Booster: Your Vibe Song")

spotify_playlists = {
    "😊 Happy": [
        "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
        "https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj",
        "https://open.spotify.com/playlist/37i9dQZF1DX0UrRvztWcAU"
    ],
    "😐 Neutral": [
        "https://open.spotify.com/playlist/37i9dQZF1DWUvHZA1zLcjW",
        "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
        "https://open.spotify.com/playlist/37i9dQZF1DWXLeA8Omikj7"
    ],
    "😔 Low": [
        "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR",
        "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
        "https://open.spotify.com/playlist/37i9dQZF1DWX83CujKHHOn"
    ]
}

if mood in spotify_playlists:
    playlist_url = random.choice(spotify_playlists[mood])
    st.markdown(f"[Click here to play a handpicked playlist 🎧]({playlist_url})")

# --- Weekly Progress Tracker ---
st.markdown("---")
st.markdown("### 📊 Weekly Progress Tracker")

week_ago = today - datetime.timedelta(days=6)
week_dates = [week_ago + datetime.timedelta(days=i) for i in range(7)]
df_all["date"] = pd.to_datetime(df_all["date"])
week_df = df_all[df_all["date"].isin(week_dates)]
week_df = week_df.sort_values("date")

chart_df = pd.DataFrame({
    "Day": week_df["date"].dt.strftime("%A (%d %b)"),
    "Habits Done": week_df["completed_habits"]
})

if not chart_df.empty:
    st.bar_chart(chart_df.set_index("Day"))
else:
    st.info("No data yet this week. Start tracking today! 🌱")

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
