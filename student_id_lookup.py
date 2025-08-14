import pandas as pd
def lookup_student_info(df, year, subject, student_id):
    # 과목별 점수 컬럼 선택
    if subject == "수학":
        score_column = "수학"
    elif subject == "영어":
        score_column = "영어"
    else:
        score_column = "과학"

    # 해당 학년의 데이터 필터링
    year_df = df[df['학년'] == year]
    
    # 학생 ID 조회
    student_info = year_df[[year_df['학생ID'] == student_id][['학생ID', '학년', '반', score_column, '석차', '등급']]]

    return student_info