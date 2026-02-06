import mysql.connector
import pandas as pd
import streamlit as st

# Database සැකසුම්
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'university_risk_db'
}

def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        return None

def init_db():
    conn = get_connection()
    if conn is None: return

    c = conn.cursor()
    # SQL වල Column නම් වලට තිත් (.) තියන්න බැරි නිසා අපි underscores (_) පාවිච්චි කරනවා
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_summary (
            registration_no VARCHAR(20) PRIMARY KEY,
            sgpa_1_1 DECIMAL(4,2),
            sgpa_1_2 DECIMAL(4,2),
            sgpa_2_1 DECIMAL(4,2),
            overall_gpa DECIMAL(4,2),
            risk_status VARCHAR(20),
            target INT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ MySQL Database initialized.")

def save_analysis(df):
    conn = get_connection()
    if conn is None: return
    c = conn.cursor()
    
    count = 0
    for _, row in df.iterrows():
        # මෙන්න මෙතනයි අපි වෙනස කරන්නේ:
        # DataFrame එකේ තියෙන්නේ 'SGPA_2.1' (Dot)
        # අපි ඒක SQL එකට යවද්දී 'sgpa_2_1' (Underscore) එකට දානවා.
        
        sql = '''
            INSERT INTO student_summary 
            (registration_no, sgpa_1_1, sgpa_1_2, sgpa_2_1, overall_gpa, risk_status, target)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            sgpa_1_1=%s, sgpa_1_2=%s, sgpa_2_1=%s, overall_gpa=%s, risk_status=%s, target=%s
        '''
        
        # අගයන් ලබා ගැනීමේදී Dot (.) භාවිතා කරන්න (DataFrame Column Names)
        s11 = row.get('SGPA_1.1', 0.0)
        s12 = row.get('SGPA_1.2', 0.0)
        s21 = row.get('SGPA_2.1', 0.0) # කලින් මෙතන තිබ්බේ SGPA_2_1, ඒකයි Error ආවේ
        
        val = (
            row['Registration_No'], s11, s12, s21,
            row['Overall_GPA'], row['Risk_Status'], row['Target'],
            # Update කොටස සඳහා
            s11, s12, s21, 
            row['Overall_GPA'], row['Risk_Status'], row['Target']
        )
        
        c.execute(sql, val)
        count += 1
        
    conn.commit()
    conn.close()
    print(f"✅ Saved {count} records.")

def fetch_all_data():
    conn = get_connection()
    if conn is None: return pd.DataFrame()

    query = "SELECT * FROM student_summary"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_risk_counts():
    conn = get_connection()
    if conn is None: return {}
    c = conn.cursor()
    c.execute("SELECT risk_status, COUNT(*) FROM student_summary GROUP BY risk_status")
    data = c.fetchall()
    conn.close()
    return dict(data)

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 👇 මෙන්න මෙතන Table එකේ නම 'student_summary' ලෙස වෙනස් කළා
        cursor.execute("TRUNCATE TABLE student_summary;") 
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error clearing data: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()