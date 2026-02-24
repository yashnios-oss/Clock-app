import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="IST Clock & Timer", layout="wide", initial_sidebar_state="collapsed")

# 1. Custom CSS for Full Screen Experience
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

/* Remove Streamlit padding and bars */
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050508;
    color: white;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
}

/* Background Glow */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #1a1a2e 0%, #050508 100%);
}

.main-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Full Viewport Height */
    width: 100vw;
    text-align: center;
}

.date-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(14px, 2vw, 24px);
    color: #6a6a9a;
    letter-spacing: 0.5em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.time-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(150px, 35vw, 500px); /* Massive Full Screen Font */
    line-height: 0.8;
    background: linear-gradient(180deg, #ffffff 30%, #4a4a8a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 50px rgba(100, 100, 255, 0.2));
}

.seconds-display {
    font-family: 'Space Mono', monospace;
    font-size: clamp(20px, 4vw, 40px);
    color: #4a4a8a;
    margin-top: 20px;
}

/* Hidden control panel that appears on hover at bottom */
.control-panel {
    position: fixed;
    bottom: 20px;
    opacity: 0.1;
    transition: opacity 0.3s;
}
.control-panel:hover { opacity: 1; }

</style>
""", unsafe_allow_html=True)

# 2. Timezone Logic (GMT +5:30)
utc_now = datetime.utcnow()
ist_offset = timedelta(hours=5, minutes=30)
ist_now = utc_now + ist_offset

# Formatting
date_str = ist_now.strftime("%A, %B %d, %Y")
hours_min = ist_now.strftime("%H:%M")
seconds = ist_now.strftime("%S")

# 3. Render Full Screen UI
st.markdown(f"""
<div class="main-wrapper">
    <div class="date-display">{date_str}</div>
    <div class="time-display">{hours_min}</div>
    <div class="seconds-display">:{seconds} <span style="font-size: 12px; letter-spacing: 2px;">IST (GMT+5:30)</span></div>
</div>
""", unsafe_allow_html=True)

# 4. Auto-Refresh Logic
# Refreshing every 1 second for the clock
time.sleep(1)
st.rerun()
