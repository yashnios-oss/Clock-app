import streamlit as st
import time
import random
from datetime import datetime, timedelta

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="Forest Focus | Rewards", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE REWARD UI (Aesthetic & High Contrast) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=Bebas+Neue&family=Space+Mono:wght@700&display=swap');

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #0a1f14 0%, #050a08 100%);
    color: #e0f2f1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }

/* Readability Overrides */
div[data-baseweb="input"], .stButton > button, div[data-baseweb="slider"], .stCheckbox {
    background-color: rgba(46, 204, 113, 0.05) !important;
    border: 1px solid rgba(46, 204, 113, 0.2) !important;
    border-radius: 15px !important;
    color: #2ecc71 !important;
}

/* Reward HUD Styling */
.reward-hud {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    padding: 15px 25px;
    margin-bottom: 25px;
    display: flex;
    justify-content: space-around;
    border: 1px solid rgba(255, 215, 0, 0.2);
}
.stat-box { text-align: center; }
.stat-val { font-family: 'Bebas Neue'; font-size: 32px; color: #ffd700; }
.stat-label { font-size: 10px; letter-spacing: 2px; color: #2ecc71; font-weight: 800; }

.zen-panel {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(40px);
    border: 1px solid rgba(46, 204, 113, 0.1);
    border-radius: 35px;
    padding: 30px;
    margin-bottom: 20px;
}

/* Forest Grid */
.forest-map {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    padding: 15px;
    background: rgba(0,0,0,0.3);
    border-radius: 20px;
}
.map-cell {
    aspect-ratio: 1;
    background: rgba(46, 204, 113, 0.03);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    border: 1px solid rgba(255,255,255,0.05);
}

.timer-text { font-family: 'Bebas Neue'; font-size: 70px; color: #2ecc71; line-height: 1; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE ENGINE (Currency & Rewards) ---
if 'seeds' not in st.session_state: st.session_state.seeds = 0 # Earned via tasks
if 'sunlight' not in st.session_state: st.session_state.sunlight = 0 # Earned via timer
if 'forest_grid' not in st.session_state: st.session_state.forest_grid = []
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'f_active' not in st.session_state: st.session_state.f_active = False
if 'f_secs' not in st.session_state: st.session_state.f_secs = 0
if 'f_total' not in st.session_state: st.session_state.f_total = 1

def get_ist():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

# --- 4. REWARD HUD ---
st.markdown(f"""
<div class="reward-hud">
    <div class="stat-box">
        <div class="stat-val">🌱 {st.session_state.seeds}</div>
        <div class="stat-label">SEEDS EARNED</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">☀ {st.session_state.sunlight}</div>
        <div class="stat-label">SUNLIGHT COLLECTED</div>
    </div>
    <div class="stat-box">
        <div class="stat-val">🌳 {len(st.session_state.forest_grid)}/25</div>
        <div class="stat-label">FOREST DENSITY</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---
now_ist = get_ist()
col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    # TASK SYSTEM WITH REWARDS
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.markdown("### 🌿 Task Nursery")
    with st.form("task_plant", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        t_in = c1.text_input("New Task", placeholder="Plant a goal (+5 Seeds)", label_visibility="collapsed")
        if c2.form_submit_button("PLANT"):
            if t_in:
                st.session_state.inventory.append({"task": t_in, "done": False, "id": time.time()})
                st.rerun()
    
    for idx, item in enumerate(st.session_state.inventory):
        t_col, d_col = st.columns([0.85, 0.15])
        if not item['done']:
            if t_col.checkbox(f"{item['task']} (+10 Seeds)", key=f"tk_{item['id']}"):
                st.session_state.inventory[idx]['done'] = True
                st.session_state.seeds += 10 # Reward for completion
                st.toast("Earned 10 Seeds! 🌱")
                st.rerun()
        else:
            t_col.markdown(f"~~{item['task']}~~ ✅")
        
        if d_col.button("🗑️", key=f"del_{item['id']}"):
            st.session_state.inventory.pop(idx)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # TIMER SYSTEM WITH REWARDS
    st.markdown('<div class="zen-panel" style="text-align:center;">', unsafe_allow_html=True)
    if not st.session_state.f_active:
        st.subheader("Basking Timer")
        mins = st.slider("Select Minutes", 5, 120, 25, step=5)
        st.caption(f"Success will earn you {mins} Sunlight ☀")
        if st.button("🚀 INITIATE PHOTOSYNTHESIS"):
            st.session_state.f_secs = mins * 60
            st.session_state.f_total = mins * 60
            st.session_state.f_active = True
            st.rerun()
    else:
        if st.button("⏹ ABANDON (Lose Progress)"):
            st.session_state.f_active = False
            st.session_state.f_secs = 0
            st.rerun()

    timer_spot = st.empty()
    while st.session_state.f_active and st.session_state.f_secs > 0:
        mm, ss = divmod(st.session_state.f_secs, 60)
        prog = (st.session_state.f_secs / st.session_state.f_total) * 100
        timer_spot.markdown(f"""
            <div style="text-align:center;">
                <div class="timer-text">{mm:02d}:{ss:02d}</div>
                <div style="color:#2ecc71; letter-spacing:3px;">GENERATING SUNLIGHT...</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
        st.session_state.f_secs -= 1
        if st.session_state.f_secs <= 0:
            st.session_state.f_active = False
            earned_sun = st.session_state.f_total // 60
            st.session_state.sunlight += earned_sun
            # Reward: A rare tree if sunlight is high
            tree_type = "✨🌲" if earned_sun >= 45 else "🌳"
            st.session_state.forest_grid.append(tree_type)
            st.balloons()
            st.rerun()

    # THE SACRED GROVE MAP
    st.markdown("<h3 style='margin-bottom:10px;'>Your Sacred Grove</h3>", unsafe_allow_html=True)
    grid_html = '<div class="forest-map">'
    for i in range(25):
        tree_icon = st.session_state.forest_grid[i] if i < len(st.session_state.forest_grid) else ""
        grid_html += f'<div class="map-cell">{tree_icon}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO REFRESH
time.sleep(0.5)
st.rerun()
