import streamlit as st
import time
from datetime import datetime, timedelta

# --- ADVANCED SESSION STATE ---
if "study_log" not in st.session_state:
    st.session_state.study_log = []
if "daily_target_hours" not in st.session_state:
    st.session_state.daily_target_hours = 8

# --- CSS FOR ENHANCED TRACKING ---
st.markdown("""
<style>
    .metric-card {
        background: rgba(20, 20, 35, 0.7);
        border: 1px solid #3a3a6a;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .goal-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #12121f;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 4px solid #624aff;
    }
    .status-badge {
        font-size: 0.8rem;
        padding: 4px 10px;
        border-radius: 20px;
        background: #2a2a4a;
        color: #9090ff;
    }
</style>
""", unsafe_allow_html=True)

# --- TRACKING DASHBOARD ---
st.title("🚀 Performance Tracker")

# 1. Top Level Metrics
col1, col2, col3 = st.columns(3)
total_tasks = len(st.session_state.study_log)
completed_tasks = sum(1 for task in st.session_state.study_log if task['status'] == 'Done')
efficiency = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

with col1:
    st.markdown(f'<div class="metric-card"><h3>Focus Score</h3><h1>{int(efficiency)}%</h1></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h3>Tasks</h3><h1>{completed_tasks}/{total_tasks}</h1></div>', unsafe_allow_html=True)
with col3:
    # Calculate total hours logged
    total_hrs = sum(task['hrs'] for task in st.session_state.study_log if task['status'] == 'Done')
    st.markdown(f'<div class="metric-card"><h3>IST Study Hours</h3><h1>{total_hrs}h</h1></div>', unsafe_allow_html=True)

st.write("---")

# 2. Add New Goal with Metadata
with st.expander("➕ Create New Study Block", expanded=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    task_name = c1.text_input("Task Description", placeholder="e.g., Organic Chemistry Revision")
    hrs_estimate = c2.number_input("Est. Hours", min_value=0.5, max_value=12.0, step=0.5)
    category = c3.selectbox("Type", ["Deep Work", "Revision", "Practice", "Lecture"])
    
    if st.button("Initialize Block"):
        if task_name:
            st.session_state.study_log.append({
                "task": task_name,
                "hrs": hrs_estimate,
                "type": category,
                "status": "In Progress",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()

# 3. Dynamic Goal List
st.subheader("Current Sprint")
for idx, item in enumerate(st.session_state.study_log):
    with st.container():
        # Change styling if done
        opacity = "0.5" if item['status'] == "Done" else "1.0"
        
        cols = st.columns([0.05, 0.5, 0.15, 0.15, 0.15])
        
        # Checkbox to complete
        if cols[0].checkbox("", value=(item['status'] == "Done"), key=f"check_{idx}"):
            st.session_state.study_log[idx]['status'] = "Done"
        else:
            st.session_state.study_log[idx]['status'] = "In Progress"
            
        cols[1].markdown(f"**{item['task']}**")
        cols[2].markdown(f"<span class='status-badge'>{item['type']}</span>", unsafe_allow_html=True)
        cols[3].write(f"⏱ {item['hrs']}h")
        
        if cols[4].button("Delete", key=f"del_{idx}"):
            st.session_state.study_log.pop(idx)
            st.rerun()
