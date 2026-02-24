import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# --- PRE-REQUISITE: SESSION STATE ---
if "study_log" not in st.session_state:
    st.session_state.study_log = []

# --- CALCULATION LOGIC ---
total_tasks = len(st.session_state.study_log)
completed_tasks = sum(1 for task in st.session_state.study_log if task['status'] == 'Done')
progress_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

# --- CSS FOR THE "APP" FEEL ---
st.markdown("""
<style>
    .tracking-card {
        background: #ffffff10;
        border-radius: 30px;
        padding: 25px;
        text-align: center;
        border: 1px solid #ffffff20;
    }
    .prediction-text {
        font-family: 'Space Mono';
        color: #8888aa;
        font-size: 0.9rem;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- CIRCULAR PROGRESS CHART ---
def create_radial_chart(percent):
    fig = go.Figure(go.Pie(
        values=[percent, 100 - percent],
        hole=0.85,
        marker_colors=['#624aff', '#1a1a2e'],
        textinfo='none',
        hoverinfo='none',
        direction='clockwise',
        sort=False
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(
            text=f"<b>{int(percent)}%</b><br><span style='font-size:12px;'>Done</span>",
            x=0.5, y=0.5, font_size=40, font_family="Bebas Neue", font_color="white", showarrow=False
        )]
    )
    return fig

# --- UI LAYOUT ---
with st.container():
    st.markdown('<div class="tracking-card">', unsafe_allow_html=True)
    
    # Render the Chart
    st.plotly_chart(create_radial_chart(progress_pct), use_container_width=True, config={'displayModeBar': False})
    
    # Status Message (Similar to "Your next period is due")
    if total_tasks == 0:
        msg = "Add your first study goal below"
    elif progress_pct < 100:
        msg = f"You have {total_tasks - completed_tasks} tasks remaining today"
    else:
        msg = "Goal Achieved! You're ahead of schedule."
        
    st.markdown(f"### {msg}")
    st.markdown('<div class="prediction-text">Keep your streak alive for 5 days to unlock Deep Work mode</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TASK MANAGEMENT (Same as previous version) ---
st.write("")
with st.expander("📝 Manage Today's Goals"):
    new_task = st.text_input("New Study Task")
    if st.button("Add"):
        st.session_state.study_log.append({"task": new_task, "status": "In Progress"})
        st.rerun()

    for idx, item in enumerate(st.session_state.study_log):
        col1, col2 = st.columns([0.8, 0.2])
        if col1.checkbox(item['task'], value=(item['status']=="Done"), key=f"t_{idx}"):
            st.session_state.study_log[idx]['status'] = "Done"
        if col2.button("🗑️", key=f"d_{idx}"):
            st.session_state.study_log.pop(idx)
            st.rerun()
