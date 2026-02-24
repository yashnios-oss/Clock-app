import streamlit as st
import time
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Study Focus IST", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050508;
    color: white;
    overflow-x: hidden;
}

/* Full Screen Clock Container */
.clock-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 70vh;
    text-align: center;
    background: radial-gradient(circle at center, #111122 0%, #050508 100%);
}

.time-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(100px, 20vw, 300px);
    line-height: 0.8;
    background: linear-gradient(180deg, #ffffff 30%, #4a4a8a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.quote-box {
    font-family: 'Space Mono', monospace;
    font-style: italic;
    color: #8888aa;
    font-size: 1.2rem;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.goal-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 5px solid #4a4a8a;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "goals" not in st.session_state:
    st.session_state.goals = []
if "quote" not in st.session_state:
    quotes = [
        "It always seems impossible until it's done.",
        "Don't stop when you're tired. Stop when you're finished.",
        "Discipline is doing what needs to be done, even if you don't want to do it.",
        "Your future self will thank you for the work you do today.",
        "The pain of discipline is far less than the pain of regret."
    ]
    st.session_state.quote = random.choice(quotes)

# --- TIME LOGIC (GMT +5:30) ---
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
time_str = ist_now.strftime("%H:%M")
seconds_str = ist_now.strftime("%S")
date_str = ist_now.strftime("%A, %B %d")

# --- UI: MAIN CLOCK & MOTIVATION ---
st.markdown(f"""
<div class="clock-wrapper">
    <div style="font-family: 'Space Mono'; color: #4a4a8a; letter-spacing: 5px;">{date_str}</div>
    <div class="time-display">{time_str}</div>
    <div style="font-family: 'Space Mono'; color: #4a4a8a;">:{seconds_str} IST</div>
    <div class="quote-box">"{st.session_state.quote}"</div>
</div>
""", unsafe_allow_html=True)

# --- UI: GOAL TRACKER SECTION ---
st.divider()
st.subheader("🎯 Daily Study Goals")

# Goal Input
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        new_goal = st.text_input("What is your focus for the next hour?", placeholder="e.g., Solve 10 Physics problems", label_visibility="collapsed")
    with col2:
        if st.button("Add Goal") and new_goal:
            st.session_state.goals.append({"task": new_goal, "done": False})
            st.rerun()

# Display Goals & Accountability
if st.session_state.goals:
    done_count = sum(1 for g in st.session_state.goals if g['done'])
    total_count = len(st.session_state.goals)
    progress = done_count / total_count
    
    st.write(f"Accountability Progress: {done_count}/{total_count} tasks completed")
    st.progress(progress)

    for idx, goal in enumerate(st.session_state.goals):
        cols = st.columns([0.1, 0.7, 0.2])
        is_done = cols[0].checkbox("", value=goal['done'], key=f"check_{idx}")
        
        # Update state if checkbox changed
        if is_done != goal['done']:
            st.session_state.goals[idx]['done'] = is_done
            st.rerun()
            
        if is_done:
            cols[1].markdown(f"~~{goal['task']}~~")
        else:
            cols[1].write(goal['task'])
            
        if cols[2].button("🗑️", key=f"del_{idx}"):
            st.session_state.goals.pop(idx)
            st.rerun()
else:
    st.info("No study goals set yet. Input a goal above to start tracking!")

# --- FOOTER AUTO-REFRESH ---
time.sleep(1)
st.rerun()
