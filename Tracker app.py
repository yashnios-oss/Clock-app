import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="DeepWork | StudyFocus OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE DESIGN ARCHITECTURE (Aesthetic & High-Contrast) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

/* Main Background - Deep Obsidian */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #1a1a3a, #050508);
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit UI Elements */
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
.block-container { padding-top: 2rem !important; max-width: 1200px; }

/* FIXING READABILITY: Comprehensive CSS Overrides */
div[data-baseweb="input"], .stButton > button, div[data-baseweb="slider"], .stCheckbox {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    color: white !important;
    transition: all 0.3s ease;
}

/* Hover effects for buttons */
.stButton > button:hover {
    border-color: #7c4dff !important;
    box-shadow: 0 0 15px rgba(124, 77, 255, 0.4);
}

/* Professional Glass Card */
.glass-panel {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 35px;
    padding: 40px;
    margin-bottom: 25px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

/* Typography Hierarchy */
.ist-label {
    font-family: 'Space Mono';
    font-size: 1rem;
    color: #7c4dff;
    letter-spacing: 5px;
    text-transform: uppercase;
    font-weight: 800;
}

.massive-ist-clock {
    font-family: 'Bebas Neue';
    font-size: 120px;
    line-height: 0.8;
    background: linear-gradient(180deg, #fff 40%, #7c4dff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 30px rgba(124, 77, 255, 0.2));
}

/* Radial Timer Styling */
.timer-container { position: relative; width: 320px; margin: 0 auto; }
.timer-center {
    position: absolute; top: 55%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Bebas Neue'; font-size: 80px;
    color: white; text-align: center; line-height: 0.7;
}

.circle-base { fill: none; stroke: rgba(255,255,255,0.03); stroke-width: 1.5; }
.circle-progress {
    fill: none; stroke: #7c4dff; stroke-width: 2;
    stroke-linecap: round; transition: stroke-dasharray 0.8s ease-in-out;
}

/* Task Checkbox Labels */
.stCheckbox label p {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #e0e0e0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'timer_seconds' not in st.session_state: st.session_state.timer_seconds = 0
if 'timer_total' not in st.session_state: st.session_state.timer_total = 1

def get_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

# --- 4. HEADER HUD ---
now = get_ist()
st.markdown(f"**{now.strftime('%A, %B %d, %Y')}**")

# --- 5. MAIN WORKSPACE ---
col_plan, col_focus = st.columns([1, 1.2], gap="large")

with col_plan:
    # IST CLOCK MODULE
    st.markdown(f"""
    <div class="glass-panel" style="text-align:center;">
        <div class="ist-label">IST Master Time</div>
        <div class="massive-ist-clock">{now.strftime('%H:%M')}<span style="font-size: 40px; color:#7c4dff;">:{now.strftime('%S')}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # GOAL INVENTORY
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🎯 Goal Inventory")
    
    with st.form("inventory_form", clear_on_submit=True):
        entry_col, btn_col = st.columns([3, 1])
        new_g = entry_col.text_input("Log Goal", placeholder="What's next?", label_visibility="collapsed")
        if btn_col.form_submit_button("ADD"):
            if new_g:
                st.session_state.tasks.append({"task": new_g, "done": False, "id": time.time()})
                st.rerun()

    st.write("---")
    for idx, item in enumerate(st.session_state.tasks):
        t_col, d_col = st.columns([0.85, 0.15])
        status = t_col.checkbox(item['task'], value=item['done'], key=f"tk_{item['id']}")
        if status != item['done']:
            st.session_state.tasks[idx]['done'] = status
            st.rerun()
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.tasks.pop(idx)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_focus:
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("<div class='ist-label' style='margin-bottom:20px;'>Focus Engine</div>", unsafe_allow_html=True)
    
    # TIMER DURATION SELECTOR
    if not st.session_state.timer_running:
        duration = st.slider("Select Session Minutes", 1, 120, 25)
        if st.button("🚀 INITIATE DEEP WORK"):
            st.session_state.timer_seconds = duration * 60
            st.session_state.timer_total = duration * 60
            st.session_state.timer_running = True
            st.rerun()
    else:
        if st.button("⏹ TERMINATE SESSION"):
            st.session_state.timer_running = False
            st.session_state.timer_seconds = 0
            st.rerun()

    # RADIAL TIMER COMPONENT
    timer_placeholder = st.empty()
    
    while st.session_state.timer_running and st.session_state.timer_seconds > 0:
        mm, ss = divmod(st.session_state.timer_seconds, 60)
        progress = (st.session_state.timer_seconds / st.session_state.timer_total) * 100
        
        timer_placeholder.markdown(f"""
        <div class="timer-container">
            <svg viewBox="0 0 36 36">
                <path class="circle-base" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="circle-progress" stroke-dasharray="{progress}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
            </svg>
            <div class="timer-center">
                {mm:02d}:{ss:02d}<br>
                <span style="font-size:14px; font-family:'Inter'; color:#7c4dff; letter-spacing:2px;">REMAINING</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        
        if st.session_state.timer_seconds <= 0:
            st.session_state.timer_running = False
            st.balloons()
            st.rerun()

    # Idle State
    if not st.session_state.timer_running:
        timer_placeholder.markdown(f"""
        <div class="timer-container">
            <svg viewBox="0 0 36 36"><path class="circle-base" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/></svg>
            <div class="timer-center" style="color:#222;">00:00</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AUTO-REFRESH ENGINE ---
time.sleep(0.5)
st.rerun()
