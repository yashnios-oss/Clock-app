import streamlit as st
import time
from datetime import datetime, timedelta

# --- APP CONFIG & THEME ---
st.set_page_config(page_title="DeepWork Focus", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Glassmorphism & Mobile App Aesthetic) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Bebas+Neue&family=Space+Mono&display=swap');

/* Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem !important; }

/* Glass Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Clock Styling */
.ist-clock {
    font-family: 'Bebas Neue', cursive;
    font-size: 120px;
    line-height: 1;
    background: linear-gradient(to bottom, #fff, #888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

/* Circular Progress Logic */
.progress-container {
    position: relative;
    width: 250px;
    height: 250px;
    margin: 0 auto;
}
.circular-chart {
  display: block;
  margin: 10px auto;
  max-width: 100%;
  max-height: 250px;
}
.circle-bg { fill: none; stroke: rgba(255,255,255,0.1); stroke-width: 2.5; }
.circle {
  fill: none; stroke-width: 2.8; stroke-linecap: round;
  transition: stroke-dasharray 1s ease;
  stroke: #624aff;
}
.percentage {
  font-family: 'Bebas Neue'; font-size: 18px; text-anchor: middle; fill: white;
}

/* Interaction Buttons */
.energy-btn {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: 0.3s;
}
.energy-btn:hover { background: rgba(98, 74, 255, 0.3); border-color: #624aff; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'energy' not in st.session_state:
    st.session_state.energy = "Neutral"

# --- TIME & DATE (IST GMT+5:30) ---
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
time_str = ist_now.strftime("%H:%M")
sec_str = ist_now.strftime("%S")
date_str = ist_now.strftime("%A, %d %B")

# --- UI LAYOUT ---

# Header Section
st.markdown(f"**{date_str}** |  {ist_now.year}")
st.title("Your Study Cycle")

col_left, col_right = st.columns([1.2, 1])

with col_left:
    # 1. THE RADIAL TRACKER (Custom SVG)
    done_count = sum(1 for t in st.session_state.tasks if t['done'])
    total_count = len(st.session_state.tasks)
    progress = (done_count / total_count * 100) if total_count > 0 else 0
    
    st.markdown(f"""
    <div class="glass-card">
        <div class="progress-container">
            <svg viewBox="0 0 36 36" class="circular-chart">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle" stroke-dasharray="{progress}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <text x="18" y="20.35" class="percentage">{int(progress)}%</text>
            </svg>
        </div>
        <div style="text-align: center; margin-top: -20px;">
            <h2 style="margin-bottom: 0;">{"Keep Going!" if progress < 100 else "Day Complete!"}</h2>
            <p style="color: #888;">{done_count} of {total_count} study blocks finished</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ENERGY TRACKER
    st.markdown('<p style="font-size: 0.9rem; color: #888;">HOW DO YOU FEEL TODAY?</p>', unsafe_allow_html=True)
    en_col1, en_col2, en_col3 = st.columns(3)
    if en_col1.button("🔥 High Focus"): st.session_state.energy = "High"
    if en_col2.button("😴 Tiring"): st.session_state.energy = "Low"
    if en_col3.button("⚖️ Balanced"): st.session_state.energy = "Neutral"

with col_right:
    # 3. CLOCK SECTION
    st.markdown(f"""
    <div class="glass-card">
        <div class="ist-clock">{time_str}<span style="font-size: 30px; color: #624aff;">:{sec_str}</span></div>
        <p style="text-align: center; font-family: 'Space Mono'; color: #624aff;">IST TIMEZONE ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

    # 4. ACCOUNTABILITY LOG
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎯 Goal Accountability")
    
    # Task Input
    with st.form("task_form", clear_on_submit=True):
        new_t = st.text_input("Define your next study sprint...", placeholder="e.g. Solve Calc III integration")
        if st.form_submit_button("Log Sprint"):
            if new_t:
                st.session_state.tasks.append({"task": new_t, "done": False})
                st.rerun()

    # Task List
    for i, t in enumerate(st.session_state.tasks):
        c1, c2 = st.columns([0.8, 0.2])
        is_done = c1.checkbox(t['task'], value=t['done'], key=f"t_{i}")
        if is_done != t['done']:
            st.session_state.tasks[i]['done'] = is_done
            st.rerun()
        if c2.button("🗑️", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 5. PREDICTIONS / MOTIVATION (Bottom Banner)
st.markdown(f"""
<div class="glass-card" style="border-left: 5px solid #624aff;">
    <p style="margin:0; font-size: 0.8rem; color: #888;">AI STUDY INSIGHT</p>
    <h3 style="margin:0;">Based on your <b>{st.session_state.energy} Energy</b>, you should prioritize {
        "Deep Work (Hard Subjects)" if st.session_state.energy == "High" else "Light Revision/Notes"
    }.</h3>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
time.sleep(1)
st.rerun()
