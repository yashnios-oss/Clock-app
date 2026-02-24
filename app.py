import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="IST Clock & Alarms", layout="wide", initial_sidebar_state="collapsed")

# 1. CSS for Full Screen UI and Slide-up Alarm Panel
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050508;
    color: white;
    overflow: hidden;
    height: 100vh;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #111122 0%, #050508 100%);
}

.main-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 90vh;
    text-align: center;
}

.date-display {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    color: #6a6a9a;
    letter-spacing: 0.5em;
    text-transform: uppercase;
}

.time-display {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(150px, 30vw, 450px);
    line-height: 0.8;
    background: linear-gradient(180deg, #ffffff 30%, #4a4a8a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Alarm Notification Overlay */
.alarm-overlay {
    position: fixed;
    top: 10%;
    background: rgba(255, 50, 50, 0.2);
    border: 2px solid #ff3232;
    padding: 20px 40px;
    border-radius: 10px;
    font-family: 'Space Mono', monospace;
    animation: pulse 1s infinite;
    z-index: 1000;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# 2. Session State for Alarms
if "alarms" not in st.session_state:
    st.session_state.alarms = []
if "alarm_triggered" not in st.session_state:
    st.session_state.alarm_triggered = False

# 3. Timezone Logic (GMT +5:30)
utc_now = datetime.utcnow()
ist_now = utc_now + timedelta(hours=5, minutes=30)
current_time_str = ist_now.strftime("%H:%M")
current_date_str = ist_now.strftime("%A, %B %d, %Y")
seconds_str = ist_now.strftime("%S")

# 4. Check Alarms
for alarm in st.session_state.alarms:
    if alarm == current_time_str and seconds_str == "00":
        st.session_state.alarm_triggered = True

# 5. Display UI
if st.session_state.alarm_triggered:
    st.markdown(f'<div class="alarm-overlay">🚨 ALARM TRIGGERED: {current_time_str} 🚨</div>', unsafe_allow_html=True)
    if st.button("DISMISS ALARM"):
        st.session_state.alarm_triggered = False
        st.rerun()

st.markdown(f"""
<div class="main-wrapper">
    <div class="date-display">{current_date_str}</div>
    <div class="time-display">{current_time_str}</div>
    <div style="color: #4a4a8a; font-family: 'Space Mono'; letter-spacing: 5px;">
        :{seconds_str} <span style="font-size: 12px;">IST</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Control Panel (Bottom)
with st.expander("Manage Alarms"):
    col1, col2 = st.columns([1, 1])
    with col1:
        new_alarm = st.time_input("Set Alarm Time", value=None)
        if st.button("Add Alarm"):
            if new_alarm:
                alarm_formatted = new_alarm.strftime("%H:%M")
                if alarm_formatted not in st.session_state.alarms:
                    st.session_state.alarms.append(alarm_formatted)
                    st.rerun()
    
    with col2:
        st.write("Active Alarms:")
        if not st.session_state.alarms:
            st.write("No alarms set.")
        for a in st.session_state.alarms:
            if st.button(f"🗑️ Remove {a}"):
                st.session_state.alarms.remove(a)
                st.rerun()

# 7. Auto-refresh
time.sleep(1)
st.rerun()
