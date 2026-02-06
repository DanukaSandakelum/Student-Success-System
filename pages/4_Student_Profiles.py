import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.db_manager import fetch_all_data

st.set_page_config(page_title="Student Profiles", page_icon="👤")

st.title("👤 Individual Student Progress")
st.markdown("Analyze the performance trajectory of a specific student.")

try:
    df = fetch_all_data()
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No data available. Please upload results first.")
    st.stop()

st.sidebar.header("🔍 Find Student")
selected_reg = st.sidebar.selectbox(
    "Select Registration No:",
    df['registration_no'].unique()
)

student = df[df['registration_no'] == selected_reg].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎓 Overall GPA", f"{student['overall_gpa']:.2f}")

with col2:
    status = student['risk_status']
    if status == "High Risk":
        st.error(f"**Status:** {status}")
    else:
        st.success(f"**Status:** {status}")

with col3:
    st.metric("Last Sem GPA (2.1)", f"{student.get('sgpa_2_1', 0):.2f}")

st.divider()

st.subheader("📈 GPA Progression")

gpa_1_1 = student.get('sgpa_1_1', 0)
gpa_1_2 = student.get('sgpa_1_2', 0)
gpa_2_1 = student.get('sgpa_2_1', 0)

chart_data = pd.DataFrame({
    'Semester': ['Sem 1.1', 'Sem 1.2', 'Sem 2.1'],
    'GPA': [gpa_1_1, gpa_1_2, gpa_2_1]
})

# Matplotlib Chart
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(chart_data['Semester'], chart_data['GPA'], marker='o', linestyle='-', color='#4CAF50', linewidth=2, markersize=8)

ax.set_ylim(0, 4.05)
ax.set_ylabel("SGPA")
ax.set_title(f"Academic Performance Trend - {selected_reg}")
ax.grid(True, linestyle='--', alpha=0.6)

for i, txt in enumerate(chart_data['GPA']):
    ax.annotate(f"{txt:.2f}", (chart_data['Semester'][i], chart_data['GPA'][i]), 
                xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')

st.pyplot(fig)

st.subheader("📋 Semester Breakdown")
st.dataframe(chart_data.set_index('Semester').T, use_container_width=True)