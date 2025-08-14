# grade_calculator.py 파일 내용 예시
import pandas as pd

def calculate_grade(total_score):
    """총점에 따라 학점을 계산합니다."""
    if total_score >= 90:
        return 1
    elif total_score >= 80:
        return 2
    elif total_score >= 70:
        return 3
    elif total_score >= 60:
        return 4
    else:
        return 5

def assign_grades(df):
    """
    학생별 총점과 평균을 계산하고, 등급을 부여합니다.

    Args:
        df (pd.DataFrame): 학생 성적 데이터가 담긴 DataFrame.
                           '수학', '영어', '과학' 컬럼이 존재해야 합니다.

    Returns:
        pd.DataFrame: 총점(total_score), 평균(average_score), 등급(grade) 컬럼이 추가된 DataFrame.
    """
    # DataFrame을 명시적으로 복사
    df_copy = df.copy()
    
    df_copy['총점'] = df_copy[['수학', '영어', '과학']].sum(axis=1) # 각 학생 총점 계산
    df_copy['평균'] = df_copy['총점'] / 3  # 각 학생 평균 계산

    # 비율 기반 등급 산정
    N = len(df_copy)
    df_sorted = df_copy.sort_values(by='총점', ascending=False).reset_index(drop=True)
    grade_boundaries = [0.10, 0.24, 0.32, 0.24, 0.10]
    grade_counts = [int(N * p) for p in grade_boundaries]
    
    # 누적 등급 리스트 생성
    grades = []
    for i, count in enumerate(grade_counts, start=1):
        grades += [i] * count
    
    # 등급 수가 부족하거나 넘칠 경우 처리
    if len(grades) < N:
        grades += [5] * (N - len(grades))
    elif len(grades) > N:
        grades = grades[:N]
    
    df_sorted['등급'] = grades

    # 원래 인덱스 순서로 복원
    df_copy['등급'] = df_sorted['등급'].values
    return df_copy


if __name__ == '__main__':
    # student_scores.csv 파일을 읽어옵니다.
    try:
        df = pd.read_csv('student_scores.csv')
    except FileNotFoundError:
        print("Error: 'student_scores.csv' file not found.")
        exit()

    # 총점, 평균, 등급 계산 함수 호출
    df_with_grades = assign_grades(df.copy()) #원본 데이터 변경 방지 위해 copy 사용

    # 결과 출력 (선택 사항 - 필요에 따라 주석 해제)
    print(df_with_grades)
