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

    # 석차 계산 (과목별)
    year_df['석차'] = year_df[score_column].rank(ascending=False, method='min').astype(int)
    student_info['석차'] = year_df[year_df['학생ID'] == student_id]['석차'].values[0]

    # 과목별 등급 계산
    from grade_calculator import assign_subject_grades
    year_df_with_subject_grades = assign_subject_grades(year_df[['학생ID', score_column]], score_column)
    student_info['과목등급'] = year_df_with_subject_grades[year_df_with_subject_grades['학생ID'] == student_id]['등급'].values[0]

    # 전체 등급(총점 기준) 계산
    from grade_calculator import assign_grades
    if not {'수학', '영어', '과학'}.issubset(year_df.columns):
        student_info['전체등급'] = None
    else:
        year_df_for_total = year_df[['학생ID', '수학', '영어', '과학']].copy()
        year_df_with_total_grades = assign_grades(year_df_for_total)
        student_info['전체등급'] = year_df_with_total_grades[year_df_with_total_grades['학생ID'] == student_id]['등급'].values[0]

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