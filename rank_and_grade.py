import pandas as pd
from grade_calculator import assign_grades
from config import GRADE_SYSTEM

def calculate_rank_and_grade(df, year, subject):
    # 과목별 점수 컬럼 선택
    if subject == "수학":
        score_column = "수학"
    elif subject == "영어":
        score_column = "영어"
    else:
        score_column = "과학"
    
    # 해당 학년의 데이터 필터링
    year_df = df[df['학년'] == year].copy()
    import pandas as pd
from grade_calculator import assign_grades
from config import GRADE_SYSTEM

def calculate_rank_and_grade(df, year, subject):
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

    # 석차 계산 (해당 학년 내에서)
    year_df['석차'] = year_df[score_column].rank(ascending=False, method='min').astype(int)

    # 과목별 등급 계산 (해당 과목 점수 기준)
    from grade_calculator import assign_subject_grades
    year_df_with_subject_grades = assign_subject_grades(year_df[['학생ID', score_column]], score_column)
    year_df['등급'] = year_df_with_subject_grades['등급'].values

    return year_df[['학생ID', '석차', '등급']]