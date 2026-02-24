import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="Forest Focus | Zen OS", page_icon="🌲", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE FOREST AESTHETIC (Zero White Boxes) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

/* Main Background - Deep Forest Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1f14 0%, #050a08 100%);
    color: #e0f2f1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* REFINED CSS: Killing all white default boxes */
div[data-baseweb="input"], .stButton > button, div[data-baseweb="slider"], .stCheckbox {
    background-color: rgba(46, 204, 113, 0.05) !important;
    border: 1px solid rgba(46, 204, 113, 0.2) !important;
    border-radius: 20px !important;
    color: #2ecc71 !important;
}

/* Make sure text is white and sharp */
input { color: white !important; font-weight: 600 !important; }
.stSlider [data-baseweb="slider"] { background-color: transparent !important; }

/* Zen Glass Panels */
.zen-panel {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(46, 204, 113, 0.1);
    border-radius: 40px;
    padding: 35px;
    margin-bottom: 20px;
}

/* Timer Ring Styling */
.forest-ring-container { position: relative; width: 320px; margin: 0 auto; }
.tree-display {
    position: absolute; top: 52%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
.timer-countdown {
    font-family: 'Bebas Neue'; font-size: 85px;
    color: #2ecc71; line-height: 0.8; margin-top: 10px;
}

.ring-bg { fill: none; stroke: rgba(255,255,255,0.03); stroke-width: 1.5; }
.ring-active {
    fill: none; stroke: #2ecc71; stroke-width: 2;
    stroke-linecap: round; transition: stroke-dasharray 1s linear;
}

/* Master Clock */
.ist-clock-small {
    font-family: 'Space Mono'; font-size: 14px; color: #2ecc71;
    letter-spacing: 4px; text-transform: uppercase; text-align: center;
}
.ist-clock-large {
    font-family: 'Bebas Neue'; font-size: 110px; text-align: center;
    background: linear-gradient(180deg, #fff, #2ecc71);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# --- 3. STATE ENGINE ---
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'f_active' not in st.session_state: st.session_state.f_active = False
if 'f_secs' not in st.session_state: st.session_state.f_secs = 0
if 'f_total' not in st.session_state: st.session_state.f_total = 1

def get_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

# --- 4. WORKSPACE LAYOUT ---
now_ist = get_ist()
col_left, col_right = st.columns([1, 1.3], gap="large")

with col_left:
    # IST MASTER MODULE
    st.markdown(f"""
    <div class="zen-panel">
        <div class="ist-clock-small">India Standard Time</div>
        <div class="ist-clock-large">{now_ist.strftime("%H:%M")}<span style="font-size:35px; opacity:0.6;">:{now_ist.strftime("%S")}</span></div>
        <p style="text-align:center; color:#666; font-weight:bold;">{now_ist.strftime("%A, %d %B")}</p>
    </div>
    """, unsafe_allow_html=True)

    # STUDY LOG
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.markdown("### 🌿 Growth Tasks")
    with st.form("task_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        t_in = c1.text_input("New Task", placeholder="Plant a goal...", label_visibility="collapsed")
        if c2.form_submit_button("PLANT"):
            if t_in:
                st.session_state.inventory.append({"task": t_in, "done": False, "id": time.time()})
                st.rerun()

    for idx, item in enumerate(st.session_state.inventory):
        t_col, d_col = st.columns([0.85, 0.15])
        st_label = f"**{item['task']}**" if not item['done'] else f"~~{item['task']}~~"
        status = t_col.checkbox(st_label, value=item['done'], key=f"tk_{item['id']}")
        if status != item['done']:
            st.session_state.inventory[idx]['done'] = status
            st.rerun()
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.inventory.pop(idx)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="zen-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:30px;'>GROW YOUR FOCUS</h3>", unsafe_allow_html=True)

    # TIMER CONTROLS
    if not st.session_state.f_active:
        mins = st.slider("Session Length (Minutes)", 1, 120, 25)
        if st.button("🚀 START GROWING"):
            st.session_state.f_secs = mins * 60
            st.session_state.f_total = mins * 60
            st.session_state.f_active = True
            st.rerun()
    else:
        if st.button("⏹ ABANDON SESSION"):
            st.session_state.f_active = False
            st.session_state.f_secs = 0
            st.rerun()

    # RADIAL PROGRESS & TREE EVOLUTION
    timer_placeholder = st.empty()
    
    while st.session_state.f_active and st.session_state.f_secs > 0:
        mm, ss = divmod(st.session_state.f_secs, 60)
        prog = (st.session_state.f_secs / st.session_state.f_total) * 100
        
        # Forest Logic: Change tree emoji based on progress
        if prog > 75: tree = "🌱"
        elif prog > 50: tree = "🌿"
        elif prog > 25: tree = "🌳"
        else: tree = "🌲"

        timer_placeholder.markdown(f"""
        <div class="forest-ring-container">
            <svg viewBox="0 0 36 36">
                <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                <path class="ring-active" stroke-dasharray="{prog}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
            </svg>
            <div class="tree-display">
                <div style="font-size: 60px;">{tree}</div>
                <div class="timer-countdown">{mm:02d}:{ss:02d}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.f_secs -= 1
        
        if st.session_state.f_secs <= 0:
            st.session_state.f_active = False
            st.balloons()
            st.rerun()

    # Idle State
    if not st.session_state.f_active:
        timer_placeholder.markdown(f"""
        <div class="forest-ring-container">
            <svg viewBox="0 0 36 36"><path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/></svg>
            <div class="tree-display">
                <div style="font-size: 60px; filter: grayscale(1);">🌲</div>
                <div class="timer-countdown" style="color:#222;">00:00</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SYSTEM REFRESH ---
time.sleep(0.5)
st.rerun()
