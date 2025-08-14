import pandas as pd
from rank_and_grade import calculate_rank_and_grade
from grade_calculator import assign_grades

def lookup_student_info(df, year, subject, student_id):
    # 과목별 점수 컬럼 선택
    if subject == "수학":
        score_column = "수학"
    elif subject == "영어":
        score_column = "영어"
    else:
        score_column = "과학"

    # 해당 학년의 데이터 필터링
    year_df = df[df['학년'] == year].copy()
    
    if year_df.empty:
        return pd.DataFrame()  # 해당 학년 데이터가 없는 경우
    
    # 학생 ID 조회
    student_info = year_df[year_df['학생ID'] == student_id].copy()
    
    if student_info.empty:
        return pd.DataFrame()  # 학생을 찾을 수 없는 경우 빈 DataFrame 반환
    
    # 석차와 등급 계산
    rank_grade_info = calculate_rank_and_grade(df, year, subject)
    if not rank_grade_info.empty:
        student_rank_grade = rank_grade_info[rank_grade_info['학생ID'] == student_id]
        if not student_rank_grade.empty:
            # DataFrame 복사 후 값 할당
            student_info = student_info.copy()
            student_info.loc[:, '석차'] = student_rank_grade['석차'].iloc[0]
            student_info.loc[:, '과목등급'] = student_rank_grade['등급'].iloc[0]
    
    # 해당 학년 내에서 전체 성적 등급 계산
    try:
        year_df_with_grades = assign_grades(year_df[['학생ID', '수학', '영어', '과학']])
        student_grades = year_df_with_grades[year_df_with_grades['학생ID'] == student_id]
        if not student_grades.empty:
            student_info.loc[:, '전체등급'] = student_grades['등급'].iloc[0]
    except Exception as e:
        print(f"전체등급 계산 중 오류: {e}")
    
    # 필요한 컬럼들이 존재하는지 확인하고 선택 (순서: 학생ID, 학년, 반, 과목성적, 석차, 과목등급, 전체등급)
    available_columns = ['학생ID', '학년']
    if '반' in student_info.columns:
        available_columns.append('반')
    available_columns.append(score_column)
    if '석차' in student_info.columns:
        available_columns.append('석차')
    if '과목등급' in student_info.columns:
        available_columns.append('과목등급')
    if '전체등급' in student_info.columns:
        available_columns.append('전체등급')
    
    return student_info[available_columns]