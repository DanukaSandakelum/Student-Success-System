import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from database.db_manager import fetch_all_data

MODEL_PATH = 'utils/student_risk_model.pkl'

def train_model():
    df = fetch_all_data()
    
    if df.empty or len(df) < 5:
        return "⚠️ Not enough data to train. Please upload more results first."

    df = df.fillna(0)
    
    X = df[['sgpa_1_1', 'sgpa_1_2']] 
    
    y = df['target']

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        if len(X_test) > 0:
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            acc_msg = f"{accuracy * 100:.2f}%"
        else:
            acc_msg = "100% (Training Data Only)"
        
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
            
        return f"✅ Model Trained Successfully! Accuracy: {acc_msg}"
        
    except Exception as e:
        return f"❌ Training Failed: {str(e)}"

def predict_risk(sgpa1, sgpa2):
    if not os.path.exists(MODEL_PATH):
        return "⚠️ Model not trained yet. Go to 'Train Model' tab."
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        prediction = model.predict([[sgpa1, sgpa2]])
        probability = model.predict_proba([[sgpa1, sgpa2]])
        
        risk_prob = probability[0][1]
        
        if prediction[0] == 1:
            return f"🚨 High Risk Detected! (Confidence: {risk_prob*100:.1f}%)"
        else:
            return f"✅ Safe Zone (Confidence: {(1-risk_prob)*100:.1f}%)"
            
    except Exception as e:
        return f"Error: {str(e)}"