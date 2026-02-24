import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="StudyFocus OS Pro", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE HIGH-CONTRAST GLASS UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

/* Global Reset */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #111122 0%, #050508 100%);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* FIXING THE WHITE BOXES: Global Input & Button Styles */
div[data-baseweb="input"], .stButton > button, div[data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border-radius: 15px !important;
}

/* Ensure text inside inputs is bright */
input { color: white !important; font-weight: 600 !important; }

/* Glass Panels */
.os-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 35px; padding: 30px; margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

/* Timer Ring Styling */
.timer-ring-container { position: relative; width: 280px; margin: 0 auto; }
.timer-text-inner {
    position: absolute; top: 55%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Bebas Neue'; font-size: 65px;
    color: #7c4dff; text-align: center; line-height: 0.8;
}

.circle-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 2; }
.circle-active {
    fill: none; stroke: #7c4dff; stroke-width: 2.5;
    stroke-linecap: round; transition: stroke-dasharray 0.5s ease;
}

/* Clock Display */
.master-clock {
    font-family: 'Bebas Neue'; font-size: 100px; text-align: center;
    background: linear-gradient(180deg, #fff, #7c4dff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ENGINE ---
if 'db' not in st.session_state: st.session_state.db = []
if 't_active' not in st.session_state: st.session_state.t_active = False
if 't_seconds' not in st.session_state: st.session_state.t_seconds = 0
if 't_total' not in st.session_state: st.session_state.t_total = 1 # Avoid div by zero

# --- 4. TIME CALCULATIONS ---
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)

# --- 5. MAIN UI LAYOUT ---
col_stats, col_timer = st.columns([1, 1.2], gap="large")

with col_stats:
    # IST Master Clock
    st.markdown(f"""
    <div class="os-card">
        <div class="master-clock">{ist_now.strftime("%H:%M")}<span style="font-size:30px; color:#7c4dff">:{ist_now.strftime("%S")}</span></div>
        <p style="text-align:center; letter-spacing:4px; color:#7c4dff; font-weight:bold;">{ist_now.strftime("%A, %d %b")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Goal Tracker
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.subheader("🎯 Active Inventory")
    with st.form("add_task", clear_on_submit=True):
        f1, f2 = st.columns([3, 1])
        new_item = f1.text_input("New Task", placeholder="Identify your next goal...", label_visibility="collapsed")
        if f2.form_submit_button("ADD"):
            if new_item:
                st.session_state.db.append({"task": new_item, "done": False, "id": time.time()})
                st.rerun()
    
    for i, item in enumerate(st.session_state.db):
        t_col, d_col = st.columns([0.85, 0.15])
        status = t_col.checkbox(item['task'], value=item['done'], key=f"check_{item['id']}")
        if status != item['done']:
            st.session_state.db[i]['done'] = status
            st.rerun()
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.db.pop(i)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_timer:
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>FOCUS CYCLE</h3>", unsafe_allow_html=True)
    
    # --- RADIAL TIMER LOGIC ---
    timer_display = st.empty()
    
    # Timer Controls
    tc1, tc2, tc3 = st.columns(3)
    if tc1.button("🧠 FOCUS (25m)"):
        st.session_state.t_seconds = 25 * 60
        st.session_state.t_total = 25 * 60
        st.session_state.t_active = True
    if tc2.button("☕ BREAK (5m)"):
        st.session_state.t_seconds = 5 * 60
        st.session_state.t_total = 5 * 60
        st.session_state.t_active = True
    if tc3.button("⏹ RESET"):
        st.session_state.t_active = False
        st.session_state.t_seconds = 0
        st.rerun()

    # The Countdown Loop
    while st.session_state.t_active and st.session_state.t_seconds > 0:
        mins, secs = divmod(st.session_state.t_seconds, 60)
        progress = (st.session_state.t_seconds / st.session_state.t_total) * 100
        
        timer_display.markdown(f"""
        <div class="timer-ring-container">
            <svg viewBox="0 0 36 36">
                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle-active" stroke-dasharray="{progress}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
            </svg>
            <div class="timer-text-inner">
                {mins:02d}:{secs:02d}<br>
                <span style="font-size:12px; font-family:'Plus Jakarta Sans'; color:#888;">REMAINING</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.t_seconds -= 1
        if st.session_state.t_seconds <= 0:
            st.session_state.t_active = False
            st.balloons()
            st.rerun()

    # Static UI when timer is off
    if not st.session_state.t_active:
        timer_display.markdown(f"""
        <div class="timer-ring-container">
            <svg viewBox="0 0 36 36"><path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/></svg>
            <div class="timer-text-inner" style="color:#444;">00:00</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh for clock
time.sleep(0.5)
st.rerun()
