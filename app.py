import streamlit as st
import time

st.set_page_config(page_title="Clock & Timer", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    height: 100vh;
    background: #0a0a0f;
    overflow: hidden;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at center, #12121f 0%, #0a0a0f 70%);
}

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.main-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    gap: 0;
}

.clock-section { text-align: center; }

.date-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(12px, 1.5vw, 18px);
    color: #4a4a6a;
    letter-spacing: 0.4em;
    text-transform: uppercase;
}

.time-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(100px, 20vw, 250px);
    line-height: 0.9;
    background: linear-gradient(180deg, #e8e8ff 0%, #9090c0 60%, #5050a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 60px rgba(120,120,255,0.15));
}

.seconds-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(16px, 2vw, 28px);
    color: #6060a0;
    letter-spacing: 0.3em;
}

.timer-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(50px, 8vw, 100px);
    color: #ff6040;
}

.timer-display.done {
    color: #ff2040;
    animation: flash 0.5s ease-in-out infinite;
}

@keyframes flash {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

.progress-bar-container {
    width: 300px;
    height: 2px;
    background: #1a1a2a;
    margin: 10px auto;
}

.progress-bar-fill {
    height: 100%;
    background: #ff6040;
    transition: width 0.5s linear;
}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "timer_duration" not in st.session_state:
    st.session_state.timer_duration = 0
if "timer_paused_remaining" not in st.session_state:
    st.session_state.timer_paused_remaining = None

# Clock Logic
now = time.localtime()
hours_str = time.strftime("%H:%M", now)
seconds_str = time.strftime("%S", now)
date_str = time.strftime("%A, %B %d %Y", now)

# Timer Logic
timer_remaining = 0
timer_class = ""
progress_pct = 0

if st.session_state.timer_running:
    elapsed = time.time() - st.session_state.timer_start
    timer_remaining = max(0, st.session_state.timer_duration - elapsed)
    if st.session_state.timer_duration > 0:
        progress_pct = (1 - timer_remaining / st.session_state.timer_duration) * 100
    if timer_remaining == 0:
        timer_class = "done"
        st.session_state.timer_running = False
else:
    if st.session_state.timer_paused_remaining is not None:
        timer_remaining = st.session_state.timer_paused_remaining
        if st.session_state.timer_duration > 0:
            progress_pct = (1 - timer_remaining / st.session_state.timer_duration) * 100
    else:
        # Initial state before starting
        timer_remaining = 0 

mins_left = int(timer_remaining) // 60
secs_left = int(timer_remaining) % 60
timer_text = f"{mins_left:02d}:{secs_left:02d}"

# UI Layout
st.markdown(f"""
<div class="main-wrapper">
    <div class="clock-section">
        <div class="date-display">{date_str}</div>
        <div class="time-display">{hours_str}</div>
        <div class="seconds-display">:{seconds_str}</div>
    </div>
    <div style="height: 2px; width: 50px; background: #3a3a6a; margin: 40px 0;"></div>
    <div class="timer-section">
        <div class="timer-display {timer_class}">{timer_text}</div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {progress_pct}%"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Controls
cols = st.columns([2, 2, 2, 2])
with cols[0]:
    m_in = st.number_input("MIN", 0, 99, 5)
with cols[1]:
    s_in = st.number_input("SEC", 0, 59, 0)
with cols[2]:
    if not st.session_state.timer_running:
        if st.button("▶ START"):
            if st.session_state.timer_paused_remaining is not None:
                # Resume
                st.session_state.timer_start = time.time()
                st.session_state.timer_duration = st.session_state.timer_paused_remaining
            else:
                # New Start
                st.session_state.timer_duration = (m_in * 60) + s_in
                st.session_state.timer_start = time.time()
            st.session_state.timer_running = True
            st.rerun()
    else:
        if st.button("Pause"):
            elapsed = time.time() - st.session_state.timer_start
            st.session_state.timer_paused_remaining = max(0, st.session_state.timer_duration - elapsed)
            st.session_state.timer_running = False
            st.rerun()

with cols[3]:
    if st.button("Reset"):
        st.session_state.timer_running = False
        st.session_state.timer_paused_remaining = None
        st.rerun()

# Auto-refresh
time.sleep(0.1)
st.rerun()
