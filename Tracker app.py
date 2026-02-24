import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="StudyFocus OS Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

[data-testid="stAppViewContainer"] { background: #050508; color: white; font-family: 'Plus Jakarta Sans', sans-serif; }
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* Glass Cards */
.os-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 35px; padding: 30px; margin-bottom: 20px;
}

/* Timer Typography */
.timer-countdown {
    font-family: 'Bebas Neue', cursive;
    font-size: 120px;
    text-align: center;
    line-height: 1;
    margin: 20px 0;
}

.focus-mode { color: #7c4dff; text-shadow: 0 0 30px rgba(124, 77, 255, 0.4); }
.break-mode { color: #00e676; text-shadow: 0 0 30px rgba(0, 230, 118, 0.4); }

/* Buttons */
.stButton > button {
    width: 100%; border-radius: 15px; font-weight: 700; text-transform: uppercase;
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED TIMER STATE ---
if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 0
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'timer_type' not in st.session_state:
    st.session_state.timer_type = "Focus" # or "Break"

# --- 3. IST CLOCK LOGIC ---
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)

# --- 4. UI LAYOUT ---
col_stats, col_timer = st.columns([1, 1.2], gap="large")

with col_stats:
    st.markdown(f"### 🗓️ {ist_now.strftime('%A, %d %B')}")
    st.markdown("""
    <div class="os-card">
        <h3 style='margin:0;'>Master Dashboard</h3>
        <p style='color:#7c4dff;'>IST: """ + ist_now.strftime("%H:%M:%S") + """</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task Management Placeholder
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.subheader("🎯 Active Goals")
    # (Previous task code would live here)
    st.info("Set your goals in the sidebar to track progress.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_timer:
    st.markdown('<div class="os-card" style="text-align:center;">', unsafe_allow_html=True)
    
    # Mode Indicator
    mode_color = "focus-mode" if st.session_state.timer_type == "Focus" else "break-mode"
    st.markdown(f"<h2 class='{mode_color}'>{st.session_state.timer_type.upper()} SESSION</h2>", unsafe_allow_html=True)
    
    # --- THE TIMER ENGINE ---
    timer_placeholder = st.empty()
    
    # Controls
    c1, c2, c3 = st.columns(3)
    if c1.button("🧠 Focus (25m)"):
        st.session_state.timer_seconds = 25 * 60
        st.session_state.timer_active = True
        st.session_state.timer_type = "Focus"
    if c2.button("☕ Break (5m)"):
        st.session_state.timer_seconds = 5 * 60
        st.session_state.timer_active = True
        st.session_state.timer_type = "Break"
    if c3.button("⏹ Reset"):
        st.session_state.timer_active = False
        st.session_state.timer_seconds = 0
        st.rerun()

    # Execution Loop
    while st.session_state.timer_active and st.session_state.timer_seconds > 0:
        mins, secs = divmod(st.session_state.timer_seconds, 60)
        timer_placeholder.markdown(f"""
            <div class="timer-countdown {mode_color}">
                {mins:02d}:{secs:02d}
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        
        if st.session_state.timer_seconds <= 0:
            st.session_state.timer_active = False
            st.balloons()
            st.rerun()
            
    # Fallback Display when idle
    if not st.session_state.timer_active:
        mins, secs = divmod(st.session_state.timer_seconds, 60)
        timer_placeholder.markdown(f"""
            <div class="timer-countdown" style="color:#333;">
                {mins:02d}:{secs:02d}
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh for clock
time.sleep(0.5)
st.rerun()
