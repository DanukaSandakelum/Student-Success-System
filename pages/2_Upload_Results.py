import streamlit as st
import pandas as pd
from utils.gpa_calculator import process_results
from database.db_manager import save_analysis, clear_all_data

st.set_page_config(page_title="Upload Results", page_icon="📂", layout="wide")

st.title("📂 Upload Semester Results")

# File Uploader
uploaded_files = st.file_uploader(
    "Choose CSV files", 
    type=['csv'], 
    accept_multiple_files=True
)

if st.button("🚀 Process & Analyze Results"):
    if uploaded_files:
        with st.spinner("Analyzing files..."):
            df_report, logs = process_results(uploaded_files)
            with st.expander("Show Processing Details (Logs)", expanded=False):
                for log in logs:
                    if "❌" in log: st.error(log)
                    elif "⚠️" in log: st.warning(log)
                    else: st.info(log)
            if not df_report.empty:
                st.success(f"✅ Successfully calculated GPA for {len(df_report)} students!")
                st.dataframe(df_report, use_container_width=True)
                csv = df_report.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Full Report as CSV",
                    data=csv,
                    file_name='student_gpa_report.csv',
                    mime='text/csv',
                )
                try:
                    save_analysis(df_report)
                    st.toast("Data saved to Database!", icon="💾")
                    st.success("✅ Data saved to Database successfully!")
                except Exception as e:
                    st.error(f"Database Error: {e}")
            
            else:
                st.error("❌ No valid student data extracted. Check the logs above.")
    else:
        st.warning("⚠️ Please upload at least one CSV file.")

st.divider()
st.subheader("⚠️ Danger Zone")
st.markdown("""
    <style>
    .danger-box {
        border: 1px solid #ff4b4b;
        padding: 20px;
        border-radius: 10px;
        background-color: #fff5f5;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="danger-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.error("🗑️ **Clear All Student Data**")
        st.write("This action will delete all records from the **'student_summary'** table. You cannot undo this.")
    
    with col2:
        if st.button("⚠️ Clear Database", type="primary"):
            st.session_state['confirm_delete'] = True
    if st.session_state.get('confirm_delete'):
        st.warning("Are you sure? All data will be lost permanently!")
        
        col_confirm_1, col_confirm_2 = st.columns(2)
        
        with col_confirm_1:
            if st.button("✅ Yes, Delete Everything"):
                if clear_all_data():
                    st.success("All data in 'student_summary' has been deleted!")
                    st.session_state['confirm_delete'] = False
                    st.rerun() # Page එක Refresh වෙයි
                else:
                    st.error("Failed to clear database.")
        
        with col_confirm_2:
            if st.button("❌ Cancel"):
                st.session_state['confirm_delete'] = False
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)