import streamlit as st
import time

st.set_page_config(page_title=“Clock & Timer”, layout=“wide”, initial_sidebar_state=“collapsed”)

st.markdown(”””

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

[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Grain overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 999;
    opacity: 0.5;
}

.main-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    gap: 0;
    padding: 20px;
}

.clock-section {
    text-align: center;
    position: relative;
}

.date-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(12px, 1.5vw, 18px);
    color: #4a4a6a;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.time-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(100px, 20vw, 280px);
    line-height: 0.9;
    background: linear-gradient(180deg, #e8e8ff 0%, #9090c0 60%, #5050a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.02em;
    filter: drop-shadow(0 0 60px rgba(120,120,255,0.15));
    transition: all 0.1s ease;
}

.seconds-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(16px, 2vw, 28px);
    color: #6060a0;
    letter-spacing: 0.3em;
    margin-top: -10px;
}

.divider {
    width: 1px;
    height: 60px;
    background: linear-gradient(180deg, transparent, #3a3a6a, transparent);
    margin: 30px auto;
}

.timer-section {
    text-align: center;
    width: 100%;
    max-width: 600px;
}

.timer-label {
    font-family: 'Space Mono', monospace;
    font-size: clamp(10px, 1.2vw, 14px);
    color: #3a3a5a;
    letter-spacing: 0.5em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.timer-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(50px, 10vw, 120px);
    line-height: 1;
    color: #ff6040;
    letter-spacing: 0.05em;
    filter: drop-shadow(0 0 30px rgba(255,96,64,0.3));
}

.timer-display.running {
    animation: pulse 1s ease-in-out infinite;
}

.timer-display.done {
    color: #ff2040;
    animation: flash 0.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; filter: drop-shadow(0 0 30px rgba(255,96,64,0.3)); }
    50% { opacity: 0.85; filter: drop-shadow(0 0 50px rgba(255,96,64,0.6)); }
}

@keyframes flash {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

.controls {
    display: flex;
    gap: 12px;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    flex-wrap: wrap;
}

.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border: 1px solid #3a3a5a !important;
    color: #8080b0 !important;
    padding: 8px 20px !important;
    border-radius: 0 !important;
    transition: all 0.2s ease !important;
    height: auto !important;
}

.stButton > button:hover {
    background: rgba(100, 100, 180, 0.1) !important;
    border-color: #8080b0 !important;
    color: #c0c0e0 !important;
}

.stNumberInput > div > div > input {
    font-family: 'Space Mono', monospace !important;
    font-size: 14px !important;
    background: transparent !important;
    border: 1px solid #2a2a4a !important;
    color: #8080b0 !important;
    border-radius: 0 !important;
    text-align: center;
}

.stNumberInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.3em !important;
    color: #3a3a5a !important;
    text-transform: uppercase !important;
}

div[data-testid="stNumberInput"] { min-width: 80px; }

.progress-bar-container {
    width: 100%;
    max-width: 600px;
    height: 2px;
    background: #1a1a2a;
    margin: 15px auto 0;
    position: relative;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #3a3a8a, #ff6040);
    transition: width 0.5s linear;
}
</style>

“””, unsafe_allow_html=True)

# Session state

if “timer_running” not in st.session_state:
st.session_state.timer_running = False
if “timer_start” not in st.session_state:
st.session_state.timer_start = None
if “timer_duration” not in st.session_state:
st.session_state.timer_duration = 0
if “timer_paused_remaining” not in st.session_state:
st.session_state.timer_paused_remaining = None
if “minutes_input” not in st.session_state:
st.session_state.minutes_input = 5
if “seconds_input” not in st.session_state:
st.session_state.seconds_input = 0

now = time.localtime()
hours = time.strftime(”%H:%M”, now)
seconds = time.strftime(”%S”, now)
date_str = time.strftime(”%A, %B %d  %Y”, now)

# Timer logic

timer_remaining = 0
timer_class = “”
progress_pct = 0

if st.session_state.timer_running and st.session_state.timer_start:
elapsed = time.time() - st.session_state.timer_start
timer_remaining = max(0, st.session_state.timer_duration - elapsed)
if st.session_state.timer_duration > 0:
progress_pct = (1 - timer_remaining / st.session_state.timer_duration) * 100
if timer_remaining == 0:
timer_class = “done”
else:
timer_class = “running”
elif st.session_state.timer_paused_remaining is not None:
timer_remaining = st.session_state.timer_paused_remaining
progress_pct = (1 - timer_remaining / max(st.session_state.timer_duration, 1)) * 100
else:
timer_remaining = st.session_state.minutes_input * 60 + st.session_state.seconds_input

mins_left = int(timer_remaining) // 60
secs_left = int(timer_remaining) % 60
timer_str = f”{mins_left:02d}:{secs_left:02d}”

st.markdown(f”””

<div class="main-wrapper">
    <div class="clock-section">
        <div class="date-display">{date_str}</div>
        <div class="time-display">{hours}</div>
        <div class="seconds-display">:{seconds}</div>
    </div>
    <div class="divider"></div>
    <div class="timer-section">
        <div class="timer-label">Timer</div>
        <div class="timer-display {timer_class}">{timer_str}</div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {progress_pct}%"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Controls

st.markdown(’<div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; padding: 10px 20px 20px;">’, unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap=“small”)

with col1:
mins = st.number_input(“MIN”, min_value=0, max_value=99, value=st.session_state.minutes_input, key=“min_inp”, step=1, label_visibility=“visible”)
with col2:
secs = st.number_input(“SEC”, min_value=0, max_value=59, value=st.session_state.seconds_input, key=“sec_inp”, step=1, label_visibility=“visible”)
with col3:
if st.button(“▶ START” if not st.session_state.timer_running else “⏸ PAUSE”):
if not st.session_state.timer_running:
if st.session_state.timer_paused_remaining is not None:
st.session_state.timer_duration = st.session_state.timer_paused_remaining
else:
st.session_state.minutes_input = mins
st.session_state.seconds_input = secs
st.session_state.timer_duration = mins * 60 + secs
st.session_state.timer_start = time.time()
st.session_state.timer_running = True
st.session_state.timer_paused_remaining = None
else:
elapsed = time.time() - st.session_state.timer_start
st.session_state.timer_paused_remaining = max(0, st.session_state.timer_duration - elapsed)
st.session_state.timer_running = False
st.rerun()
with col4:
if st.button(“⏹ RESET”):
st.session_state.timer_running = False
st.session_state.timer_start = None
st.session_state.timer_paused_remaining = None
st.session_state.minutes_input = mins
st.session_state.seconds_input = secs
st.rerun()
with col5:
pass

st.markdown(’</div>’, unsafe_allow_html=True)

# Auto-refresh

if st.session_state.timer_running and timer_remaining > 0:
time.sleep(0.5)
st.rerun()
elif not st.session_state.timer_running:
time.sleep(1)
st.rerun()
