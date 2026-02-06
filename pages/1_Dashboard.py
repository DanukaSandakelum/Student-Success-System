import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database.db_manager import fetch_all_data

# Page Setup
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Student Performance Analytics")
st.markdown("Overview of student performance across semesters.")

try:
    df = fetch_all_data()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No data available. Please upload results in the 'Upload Results' page.")
    st.stop()

st.sidebar.header("🔍 Filters")
selected_status = st.sidebar.multiselect(
    "Filter by Risk Status:",
    options=df["risk_status"].unique(),
    default=df["risk_status"].unique()
)

# Filter Logic
filtered_df = df[df["risk_status"].isin(selected_status)]

total_students = len(df)
high_risk_count = len(df[df['risk_status'] == 'High Risk'])
safe_count = len(df[df['risk_status'] == 'Safe'])
avg_gpa = df['overall_gpa'].mean()

col1, col2, col3, col4 = st.columns(4)
high_risk_count = len(df[df['risk_status'] == 'High Risk'])
safe_count = len(df[df['risk_status'] == 'Safe'])
avg_gpa = df['overall_gpa'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("✅ Safe Zone", safe_count, delta=f"{safe_count/total_students*100:.1f}%")
col3.metric("🚨 High Risk", high_risk_count, delta=f"-{high_risk_count}", delta_color="inverse")
col4.metric("📈 Average GPA", f"{avg_gpa:.2f}")

st.markdown("---")

c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("Risk Distribution")
    # Pie Chart
    if not filtered_df.empty:
        status_counts = filtered_df['risk_status'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        
        # Colors: Green for Safe, Red for Risk
        colors = ['#66bb6a', '#ef5350'] if 'Safe' in status_counts.index else ['#ef5350']
        if len(status_counts) == 2: colors = ['#66bb6a', '#ef5350'] # Safe first usually
        
        ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.axis('equal')
        st.pyplot(fig1)
    else:
        st.info("No data for selected filter.")

with c2:
    st.subheader("GPA Distribution (Histogram)")
    # GPA Histogram
    if not filtered_df.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.histplot(filtered_df['overall_gpa'], bins=20, kde=True, color="skyblue", ax=ax2)
        ax2.set_xlabel("Overall GPA")
        ax2.set_ylabel("Number of Students")
        ax2.axvline(2.0, color='red', linestyle='--', label='Risk Cutoff (2.0)')
        ax2.legend()
        st.pyplot(fig2)

st.markdown("---")

st.subheader(f"📋 Student List ({len(filtered_df)} Students)")

def highlight_risk(val):
    color = '#ffcccc' if val == 'High Risk' else '#ccffcc'
    return f'background-color: {color}'

display_cols = ['registration_no', 'sgpa_1_1', 'sgpa_1_2', 'sgpa_2_1', 'overall_gpa', 'risk_status']

st.dataframe(
    filtered_df[display_cols].style.applymap(highlight_risk, subset=['risk_status']),
    use_container_width=True
)

# CSV Download Button for Filtered Data
csv = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered List",
    data=csv,
    file_name="filtered_student_list.csv",
    mime="text/csv"
)