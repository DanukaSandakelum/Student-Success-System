import pandas as pd
import io

SUBJECT_CONFIG = [
    # --- Semester 1.1 ---
    {'keyword': 'FundamentalsofComputerProgramming', 'sem': '1.1', 'credits': 4},
    {'keyword': 'FundamentalsofWebTechnologies', 'sem': '1.1', 'credits': 2},
    {'keyword': 'EssentialofICT', 'sem': '1.1', 'credits': 4},
    {'keyword': 'data', 'sem': '1.1', 'credits': 4},
    {'keyword': 'MathamaticsforTechnology', 'sem': '1.1', 'credits': 3},
    {'keyword': 'PrinciplesofManagement', 'sem': '1.1', 'credits': 2},

    # --- Semester 1.2 ---
    {'keyword': 'AdvancedComputerProgramming', 'sem': '1.2', 'credits': 4},
    {'keyword': 'DataStructures', 'sem': '1.2', 'credits': 3},
    {'keyword': 'HumanComputerInteraction', 'sem': '1.2', 'credits': 3},
    {'keyword': 'StatisticsforTechnology', 'sem': '1.2', 'credits': 2},
    

    # --- Semester 2.1 ---
    {'keyword': 'AdvancedWebTechnologies', 'sem': '2.1', 'credits': 2},
    {'keyword': 'ComputerArchitecture', 'sem': '2.1', 'credits': 3},
    {'keyword': 'InformationSecurity', 'sem': '2.1', 'credits': 2},
    {'keyword': 'MultimediaDesignandTechnologies', 'sem': '2.1', 'credits': 2},    
    {'keyword': 'SocialandProfessionalIssues', 'sem': '2.1', 'credits': 2},
    {'keyword': 'SoftwareEngineering', 'sem': '2.1', 'credits': 3},
]

GRADE_POINTS = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'E': 0.0
}

def get_gpv(grade):
    if pd.isna(grade): return 0.0
    g = str(grade).strip().upper()
    if 'ABSENT' in g or 'AB' == g or 'MC' in g: return 0.0
    if g in GRADE_POINTS: return GRADE_POINTS[g]
    for k in sorted(GRADE_POINTS.keys(), key=len, reverse=True):
        if g.startswith(k): return GRADE_POINTS[k]
    return 0.0

def clean_filename(name):
    return name.replace(" ", "").replace(".csv", "").replace("_", "").replace("-", "")

def read_csv_bulletproof(uploaded_file):
    encodings = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']
    
    content = uploaded_file.getvalue()
    
    for enc in encodings:
        try:
            return pd.read_csv(io.BytesIO(content), header=None, encoding=enc)
        except UnicodeDecodeError:
            continue
            
    return pd.read_csv(io.BytesIO(content), header=None, encoding='utf-8', errors='replace')

def process_results(uploaded_files):
    student_data = {}
    logs = [] 

    for uploaded_file in uploaded_files:
        raw_name = uploaded_file.name
        clean_name = clean_filename(raw_name)
        
        # 1. විෂය හඳුනාගැනීම
        matched_subject = None
        for sub in SUBJECT_CONFIG:
            # Case-insensitive matching
            if sub['keyword'].lower() in clean_name.lower():
                matched_subject = sub
                break
        
        if not matched_subject:
            logs.append(f"⚠️ Skipped: '{raw_name}' (Subject Name not found in Config)")
            continue
            
        logs.append(f"✅ Processing: {raw_name} -> Sem {matched_subject['sem']}")
        
        try:
            df_temp = read_csv_bulletproof(uploaded_file)
            
            header_idx = 0
            found_header = False
            for i, row in df_temp.iterrows():
                row_str = row.astype(str).str.cat(sep=' ').lower()
                if 'reg' in row_str and 'no' in row_str:
                    header_idx = i
                    found_header = True
                    break
            
            if not found_header:
                logs.append(f"❌ Error in {raw_name}: Could not find 'Reg No' header row.")
                continue

            df = df_temp.iloc[header_idx+1:].copy()
            df.columns = df_temp.iloc[header_idx].astype(str).str.strip()
            
            reg_col = next((c for c in df.columns if 'Reg' in c and 'No' in c), None)
            grade_col = next((c for c in df.columns if 'Final' in c or 'Grade' in c), None)
            
            if not reg_col or not grade_col:
                logs.append(f"❌ Error in {raw_name}: Required columns (Reg No, Final/Grade) missing.")
                continue

            count = 0
            for _, row in df.iterrows():
                reg = str(row[reg_col]).strip().replace(" ", "").replace("\n", "")
                
                if '/' not in reg: continue 
                
                if reg not in student_data:
                    student_data[reg] = {
                        '1.1_points': 0, '1.1_credits': 0,
                        '1.2_points': 0, '1.2_credits': 0,
                        '2.1_points': 0, '2.1_credits': 0,
                        'total_points': 0, 'total_credits': 0
                    }
                
                gpv = get_gpv(row[grade_col])
                credits = matched_subject['credits']
                sem = matched_subject['sem']
                
                if credits > 0:
                    weighted_gpv = gpv * credits
                    student_data[reg][f'{sem}_points'] += weighted_gpv
                    student_data[reg][f'{sem}_credits'] += credits
                    student_data[reg]['total_points'] += weighted_gpv
                    student_data[reg]['total_credits'] += credits
                count += 1
            
            logs.append(f"   -> Extracted data for {count} students.")

        except Exception as e:
            logs.append(f"❌ Critical Error processing {raw_name}: {str(e)}")

    report_list = []
    for reg, data in student_data.items():
        row = {'Registration_No': reg}
        
        # SGPA 1.1
        if data['1.1_credits'] > 0:
            row['SGPA_1.1'] = round(data['1.1_points'] / data['1.1_credits'], 2)
        else:
            row['SGPA_1.1'] = 0.0
            
        # SGPA 1.2
        if data['1.2_credits'] > 0:
            row['SGPA_1.2'] = round(data['1.2_points'] / data['1.2_credits'], 2)
        else:
            row['SGPA_1.2'] = 0.0

        # SGPA 2.1
        if data['2.1_credits'] > 0:
            row['SGPA_2.1'] = round(data['2.1_points'] / data['2.1_credits'], 2)
        else:
            row['SGPA_2.1'] = 0.0
        
        # Overall GPA
        if data['total_credits'] > 0:
            row['Overall_GPA'] = round(data['total_points'] / data['total_credits'], 2)
        else:
            row['Overall_GPA'] = 0.0
            
        # Risk Status
        if row['Overall_GPA'] < 2.0:
            row['Risk_Status'] = 'High Risk'
            row['Target'] = 1
        else:
            row['Risk_Status'] = 'Safe'
            row['Target'] = 0
            
        report_list.append(row)
        
    return pd.DataFrame(report_list), logs