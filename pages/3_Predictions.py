import streamlit as st
from utils.ml_model import train_model, predict_risk
from database.db_manager import fetch_all_data

st.set_page_config(page_title="Predictions", page_icon="🤖")

st.title("🤖 AI Risk Prediction")
st.markdown("Predict future performance based on Semester 1 results.")

try:
    df = fetch_all_data()
except:
    df = pd.DataFrame()

tab1, tab2 = st.tabs(["🔮 Predict Risk", "⚙️ Train AI Model"])

# --- Tab 1: Predict  ---
with tab1:
    st.subheader("Predict Student Status")
    
    method = st.radio(
        "How do you want to predict?",
        ["Select Existing Student", "Manual Entry"],
        horizontal=True
    )
    
    sgpa_1 = 0.0
    sgpa_2 = 0.0
    ready_to_predict = False
    
    if method == "Select Existing Student":
        if df.empty:
            st.warning("⚠️ No student data found. Please upload results first.")
        else:
            selected_reg = st.selectbox(
                "Select Registration No:", 
                df['registration_no'].unique()
            )
            
            student = df[df['registration_no'] == selected_reg].iloc[0]
            sgpa_1 = student['sgpa_1_1']
            sgpa_2 = student['sgpa_1_2']
            
            st.info(f"👤 **Student:** {selected_reg} | 📊 **SGPA 1.1:** {sgpa_1} | 📊 **SGPA 1.2:** {sgpa_2}")
            ready_to_predict = True

    else:
        c1, c2 = st.columns(2)
        with c1:
            sgpa_1 = st.number_input("SGPA Semester 1.1", min_value=0.0, max_value=4.0, step=0.01, value=2.5)
        with c2:
            sgpa_2 = st.number_input("SGPA Semester 1.2", min_value=0.0, max_value=4.0, step=0.01, value=2.5)
        ready_to_predict = True
    
    st.divider()
    if ready_to_predict:
        if st.button("🔮 Predict Risk", type="primary", use_container_width=True):
            if sgpa_1 == 0 and sgpa_2 == 0:
                st.warning("GPA values appear to be 0.0. Please check the data.")
            else:
                with st.spinner("Analyzing..."):
                    result = predict_risk(sgpa_1, sgpa_2)
                    
                    if "High Risk" in result:
                        st.error(result)
                        st.warning("⚠️ Recommendation: Provide extra academic support and counseling.")
                    elif "Safe" in result:
                        st.success(result)
                        st.balloons()
                    else:
                        st.warning(result)

# --- Tab 2: Train Model  ---
with tab2:
    st.subheader("⚙️ Model Training")
    st.write("When you upload new data, re-train the model to make it smarter.")
    
    st.metric("Available Records for Training", len(df) if not df.empty else 0)
    
    if st.button("🚀 Train New Model"):
        with st.spinner("Training AI Model..."):
            msg = train_model()
            if "Success" in msg:
                st.success(msg)
            else:
                st.error(msg)