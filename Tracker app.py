import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="StudyFocus OS v2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE ULTIMATE UI (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

/* Global Reset */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #1a1a3a 0%, #050508 100%);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* Dashboard Glass Panels */
.os-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 40px;
    padding: 35px;
    margin-bottom: 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

/* Typography Overrides */
h1, h2, h3 { font-weight: 800 !important; color: white !important; }

/* The Massive Clock */
.massive-clock {
    font-family: 'Bebas Neue', cursive;
    font-size: clamp(100px, 15vw, 220px);
    line-height: 0.85;
    text-align: center;
    background: linear-gradient(180deg, #FFFFFF 0%, #7c4dff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 40px rgba(124, 77, 255, 0.3));
}

/* High Contrast Input */
div[data-baseweb="input"] {
    background: rgba(0,0,0,0.4) !important;
    border: 2px solid #7c4dff !important;
    border-radius: 15px !important;
}
input { color: #ffffff !important; font-size: 1.2rem !important; }

/* Circular UI Styling */
.chart-container { position: relative; width: 300px; margin: auto; }
.circle-label {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

/* Task Checkbox High Contrast */
.stCheckbox label p {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
if 'db' not in st.session_state:
    st.session_state.db = []
if 'pomodoro' not in st.session_state:
    st.session_state.pomodoro = {"active": False, "start": None, "type": "Focus"}
if 'energy_log' not in st.session_state:
    st.session_state.energy_log = "Neutral"

# --- 4. ENGINE FUNCTIONS ---
def get_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

ist_now = get_ist()
time_main = ist_now.strftime("%H:%M")
time_sec = ist_now.strftime("%S")
date_display = ist_now.strftime("%A, %B %d")

# --- 5. TOP HUD (STATUS BAR) ---
hud_left, hud_center, hud_right = st.columns([1, 2, 1])
with hud_left:
    st.markdown(f"🔋 Energy: **{st.session_state.energy_log}**")
with hud_center:
    st.markdown(f"<p style='text-align:center; letter-spacing:3px; color:#7c4dff;'><b>SYSTEM STATUS: ACTIVE</b></p>", unsafe_allow_html=True)
with hud_right:
    st.markdown(f"<p style='text-align:right;'>{date_display}</p>", unsafe_allow_html=True)

# --- 6. MAIN WORKSPACE ---
col_stats, col_action = st.columns([1, 1.2], gap="large")

with col_stats:
    # --- RADIAL PROGRESS ---
    completed = sum(1 for x in st.session_state.db if x['done'])
    total = len(st.session_state.db)
    progress = (completed / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div class="os-card">
        <div class="chart-container">
            <svg viewBox="0 0 36 36" style="display: block; width: 100%;">
                <path style="fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 2;" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path style="fill: none; stroke: #7c4dff; stroke-width: 2.5; stroke-dasharray: {progress}, 100; stroke-linecap: round;" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
            </svg>
            <div class="circle-label">
                <h1 style="margin:0; font-size: 50px;">{int(progress)}%</h1>
                <p style="color:#7c4dff; margin:0; font-weight:800;">DONE</p>
            </div>
        </div>
        <div style="text-align:center; margin-top:20px;">
            <p style="font-size:1.5rem;"><b>{completed} / {total}</b> Blocks Logged</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- POMODORO TIMER ---
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("### ⏲️ Focus Timer")
    p_col1, p_col2 = st.columns(2)
    if p_col1.button("🚀 START FOCUS (25m)"):
        st.session_state.pomodoro = {"active": True, "start": time.time(), "type": "Focus"}
    if p_col2.button("☕ BREAK"):
        st.session_state.pomodoro = {"active": True, "start": time.time(), "type": "Break"}
    
    if st.session_state.pomodoro["active"]:
        rem = 1500 - (time.time() - st.session_state.pomodoro["start"])
        if rem > 0:
            st.warning(f"Session Active: {int(rem//60)}m {int(rem%60)}s remaining")
        else:
            st.success("Session Complete! Time to switch.")
            st.session_state.pomodoro["active"] = False
    st.markdown('</div>', unsafe_allow_html=True)

with col_action:
    # --- BIG CLOCK ---
    st.markdown(f"""
    <div class="os-card">
        <div class="massive-clock">{time_main}<span style="font-size: 60px; color: #7c4dff; opacity:0.8;">:{time_sec}</span></div>
        <p style="text-align: center; letter-spacing: 5px; color: #7c4dff; font-weight: bold;">IST MASTER TIME</p>
    </div>
    """, unsafe_allow_html=True)

    # --- GOAL TRACKER ---
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Study Inventory")
    
    with st.form("task_engine", clear_on_submit=True):
        f1, f2 = st.columns([3, 1])
        new_item = f1.text_input("Task Label", placeholder="What are we conquering?", label_visibility="collapsed")
        if f2.form_submit_button("ADD"):
            if new_item:
                st.session_state.db.append({"task": new_item, "done": False, "id": time.time()})
                st.rerun()

    st.write("---")
    for i, item in enumerate(st.session_state.db):
        t_col, d_col = st.columns([0.8, 0.2])
        status = t_col.checkbox(f"**{item['task']}**", value=item['done'], key=f"it_{item['id']}")
        if status != item['done']:
            st.session_state.db[i]['done'] = status
            st.rerun()
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.db.pop(i)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. ENERGY TRACKER & INSIGHTS ---
st.markdown("### Brain Power Status")
e_cols = st.columns(4)
if e_cols[0].button("🔋 PEAK"): st.session_state.energy_log = "Peak"
if e_cols[1].button("⚡ STEADY"): st.session_state.energy_log = "Steady"
if e_cols[2].button("🪫 DRAINING"): st.session_state.energy_log = "Draining"
if e_cols[3].button("🌙 SLEEPY"): st.session_state.energy_log = "Sleepy"

# --- 8. REFRESH CORE ---
time.sleep(1)
st.rerun()
