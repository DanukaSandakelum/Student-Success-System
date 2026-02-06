import streamlit as st
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Student Success System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        color: blue;
        margin-top: 50px;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<h2 class="main-title">🎓 University Student Success System</h2>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-Powered Analytics for Academic Excellence</p>', unsafe_allow_html=True)

st.divider()



st.divider()

# 5. Features Grid with Navigation Links
st.subheader("🚀 Quick Navigation")

col1, col2, col3, col4,col5 = st.columns(5)

with col1:
    st.info("📊 **Dashboard**")
    st.write("View Dashboard stats.")
    # Link to Dashboard Page
    st.page_link("pages/1_Dashboard.py", label="Go to Dashboard", icon="📊")

with col2:
    st.warning("📂 **Data Management**")
    st.write("Upload new result sheets.")
    # Link to Upload Page (Confirm your filename is 2_Upload_Results.py)
    st.page_link("pages/2_Upload_Results.py", label="Upload Results", icon="📂")

with col3:
    st.error("🤖 **AI Predictions**")
    st.write("Predict student risks.")
    # Link to Predictions Page
    st.page_link("pages/3_Predictions.py", label="AI Predictions", icon="🤖")

with col4:
    st.success("📄 **Auto Reports**")
    st.write("Download warning letters.")
    # Link to Reports Page
    st.page_link("pages/5_Reports.py", label="Get Reports", icon="📄")

with col5:
    st.success("👤 **Student Profiles**")
    st.write("Viewstudent profiles.")
    # Link to Student Profiles Page
    st.page_link("pages/4_Student_Profiles.py", label="View Profiles", icon="👤")
    



# 6. How it Works Section
st.divider()
st.subheader("💡 System Workflow")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.write("1️⃣ **Upload**")
    st.caption("Upload CSV results to update database.")

with step2:
    st.write("2️⃣ **Train**")
    st.caption("Train the AI model with new data.")

with step3:
    st.write("3️⃣ **Analyze**")
    st.caption("Check Dashboards & Student Profiles.")

with step4:
    st.write("4️⃣ **Act**")
    st.caption("Generate PDF letters for at-risk students.")

# 7. Footer (Updated Name)
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        Developed by <b>Danuka S Sandakelum</b> | © 2026 <br>
        University Student Success Project
    </div>
    """, 
    unsafe_allow_html=True
)