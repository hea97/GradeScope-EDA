import pandas as pd

def calculate_rank_and_grade(df, year, subject):
    # 과목별 점수 컬럼 선택
    if subject == "수학":
        score_column = "수학"
    elif subject == "영어":
        score_column = "영어"
    else:
        score_column = "과학"
    
    # 해당 학년의 데이터 필터링
    year_df = df[df['학년'] == year]

    # 석차 계산
    year_df['석차'] = year_df[score_column].rank(ascending=False).astype(int)

    # 등급 계산
    year_df['등급'] = year_df[score_column].apply(lambda x: calculate_grade(x, GEADE_SYSTEM))

    return year_df[['학생ID', '석차', '등급']]