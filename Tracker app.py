import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="StudyFocus OS Flexible", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE HIGH-CONTRAST UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #0f0f1f 0%, #050508 100%);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* Readability Overrides */
div[data-baseweb="input"], .stButton > button, div[data-baseweb="slider"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border-radius: 12px !important;
}

input { color: white !important; font-weight: 600 !important; }

/* Glass Card */
.os-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px; padding: 25px; margin-bottom: 20px;
}

/* Radial Timer Elements */
.timer-ring-wrapper { position: relative; width: 300px; margin: 0 auto; }
.timer-center-text {
    position: absolute; top: 52%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Bebas Neue'; font-size: 75px;
    color: #a389ff; text-align: center; line-height: 0.8;
}

.circle-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 2; }
.circle-active {
    fill: none; stroke: #7c4dff; stroke-width: 2.2;
    stroke-linecap: round; transition: stroke-dasharray 1s linear;
}

.master-clock-font {
    font-family: 'Bebas Neue'; font-size: 90px; text-align: center;
    color: #ffffff; margin: 0;
}
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'db' not in st.session_state: st.session_state.db = []
if 't_active' not in st.session_state: st.session_state.t_active = False
if 't_seconds' not in st.session_state: st.session_state.t_seconds = 0
if 't_total' not in st.session_state: st.session_state.t_total = 1

# --- 4. TIME LOGIC ---
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)

# --- 5. UI LAYOUT ---
col_stats, col_timer = st.columns([1, 1.3], gap="large")

with col_stats:
    # IST Master Clock
    st.markdown(f"""
    <div class="os-card">
        <div class="master-clock-font">{ist_now.strftime("%H:%M")}<span style="font-size:30px; color:#7c4dff">:{ist_now.strftime("%S")}</span></div>
        <p style="text-align:center; letter-spacing:4px; color:#7c4dff; font-weight:bold; margin:0;">{ist_now.strftime("%A, %d %b")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Goal Tracker
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.subheader("🎯 Goals")
    with st.form("goal_form", clear_on_submit=True):
        f1, f2 = st.columns([3, 1])
        new_g = f1.text_input("Task", placeholder="Identify your next goal...", label_visibility="collapsed")
        if f2.form_submit_button("ADD"):
            if new_g:
                st.session_state.db.append({"task": new_g, "done": False, "id": time.time()})
                st.rerun()
    
    for i, item in enumerate(st.session_state.db):
        t_col, d_col = st.columns([0.85, 0.15])
        status = t_col.checkbox(item['task'], value=item['done'], key=f"ch_{item['id']}")
        if status != item['done']:
            st.session_state.db[i]['done'] = status
            st.rerun()
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.db.pop(i)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_timer:
    st.markdown('<div class="os-card" style="text-align:center;">', unsafe_allow_html=True)
    st.subheader("⚡ FLEXIBLE FOCUS")
    
    # --- FLEXIBLE INPUT ---
    # User can set minutes here
    if not st.session_state.t_active:
        custom_mins = st.slider("Set Duration (Minutes)", min_value=1, max_value=180, value=25)
        if st.button("🚀 START FOCUS SESSION"):
            st.session_state.t_seconds = custom_mins * 60
            st.session_state.t_total = custom_mins * 60
            st.session_state.t_active = True
            st.rerun()
    else:
        if st.button("⏹ STOP & RESET"):
            st.session_state.t_active = False
            st.session_state.t_seconds = 0
            st.rerun()

    # --- RADIAL TIMER RENDER ---
    timer_area = st.empty()
    
    while st.session_state.t_active and st.session_state.t_seconds > 0:
        mins, secs = divmod(st.session_state.t_seconds, 60)
        # Calculate dasharray (percentage of ring)
        progress = (st.session_state.t_seconds / st.session_state.t_total) * 100
        
        timer_area.markdown(f"""
        <div class="timer-ring-wrapper">
            <svg viewBox="0 0 36 36">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle-active" stroke-dasharray="{progress}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
            </svg>
            <div class="timer-center-text">
                {mins:02d}:{secs:02d}
                <div style="font-size:14px; font-family:'Plus Jakarta Sans'; color:#666; letter-spacing:2px; margin-top:5px;">RUNNING</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.t_seconds -= 1
        
        if st.session_state.t_seconds <= 0:
            st.session_state.t_active = False
            st.balloons()
            st.rerun()

    # Display Idle State
    if not st.session_state.t_active:
        timer_area.markdown(f"""
        <div class="timer-ring-wrapper">
            <svg viewBox="0 0 36 36"><path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/></svg>
            <div class="timer-center-text" style="color:#333;">00:00</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh for master clock
time.sleep(0.5)
st.rerun()
