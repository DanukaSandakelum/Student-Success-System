import streamlit as st
import pandas as pd
from database.db_manager import fetch_all_data
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Risk Reports", page_icon="📄")

st.title("📄 Generate Warning Letters")
st.markdown("Download official warning letters for **High Risk** students.")

def create_pdf(reg_no, gpa):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 1*inch, "UNIVERSITY DEPARTMENT OF TECHNOLOGY")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 1.3*inch, "Student Performance Monitoring Unit")
    c.line(1*inch, height - 1.5*inch, width - 1*inch, height - 1.5*inch)

    # Details 
    c.setFont("Helvetica", 11)
    c.drawString(1*inch, height - 2.5*inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(1*inch, height - 2.8*inch, f"Registration No: {reg_no}")
    
    # Subject
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 3.5*inch, "SUBJECT: ACADEMIC PERFORMANCE WARNING")

    # Body
    c.setFont("Helvetica", 11)
    text_content = f"""
    Dear Student (Reg No: {reg_no}),

    This letter is to formally inform you that your academic performance has been flagged 
    as 'High Risk' based on your current GPA of {gpa:.2f}.

    The university requires students to maintain a satisfactory academic standing. 
    We strongly recommend that you meet with your academic advisor immediately 
    to discuss a study plan to improve your grades.

    Sincerely,

    (Signed)
    ____________________
    Head of Department
    """
    
    text_object = c.beginText(1*inch, height - 4.5*inch)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(16)
    for line in text_content.split('\n'):
        text_object.textLine(line.strip())
    c.drawText(text_object)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


try:
    df = fetch_all_data()
except Exception as e:
    st.error("Database Connection Error!")
    st.stop()

if df.empty:
    st.warning("No data found.")
    st.stop()

# --- 3. High Risk Filtering ---

# Risk Status 
if 'risk_status' not in df.columns:
    df['risk_status'] = df['overall_gpa'].apply(lambda x: 'High Risk' if x < 2.5 else 'Low Risk')

risk_students = df[df['risk_status'] == 'High Risk']

if risk_students.empty:
    st.success("🎉 No 'High Risk' students found!")
else:
    st.error(f"⚠️ Found {len(risk_students)} High Risk Student(s)")
    
   
    reg_col = 'registration_no'
    if 'registration_no' not in df.columns:
       
         reg_col = df.columns[0]
    
   
    st.dataframe(risk_students[[reg_col, 'overall_gpa', 'risk_status']], use_container_width=True)

    st.divider()
    st.subheader("📥 Download Letters")

    for index, row in risk_students.iterrows():
        col1, col2 = st.columns([3, 1])
        
        student_reg = row[reg_col]
        student_gpa = row['overall_gpa']

        with col1:
          
            st.write(f"🆔 **{student_reg}** - GPA: {student_gpa:.2f}")
        
        with col2:
           
            pdf_file = create_pdf(student_reg, student_gpa)
            
            st.download_button(
                label="📄 PDF",
                data=pdf_file,
                file_name=f"Warning_{student_reg}.pdf",
                mime="application/pdf",
                key=student_reg
            )
        st.markdown("---")