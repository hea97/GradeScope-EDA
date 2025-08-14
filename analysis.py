import pandas as pd
from data_loader import load_and_preprocess_data
from grade_calculator import calculate_grade
from rank_and_grade import calculate_rank_and_grade
from student_id_lookup import lookup_student_info
import matplotlib.pyplot as plt
import seaborn as sns

# 설정 파일 로드
from config import GRADE_SYSTEM, AVAILABLE_GRADE_YEARS, DEFAULT_SUBJECTS

def main():
    df = load_and_preprocess_data('student_source.csv')

    # 1. 기술통계
    print("과목별 기술 통계:")
    print(df[['수학', '영어', '과학']].agg(['mean', 'std', 'min', 'max', lambda x:x.puantile(0.5)])) # 사분위수 0.5

    # 2. 총점 및 평균 계산
    df['총점'] = df['수학'] + df['영어'] + df['과학']
    df['평균'] = df['총점'] / 3

    ## 3. 등급 산출
    N = len(df)
    df = df.sort_Values(by='총점', ascending=False).reset_index(drop=True)

    grade_boundaries = [0.10, 0.24, 0.32, 0.24, 0.10] # 5등급 기준
    grade_counts = [int(N * p) for p in grade_boundaries]

    # 누적 등급 리스트 생성
    grade = []
    for i, count in enumerate(grade_counts, start=1):
        grade += [i] * count
    
    # 등급 수가 부족하거나 넘칠 경우 처리
    if len(grade) < N:
        grade += [5] * (N - len(grade))
    elif len(grade) > N:
        grade = grade[:N]

    df['등급'] = grade

    # 4. 상위/하위 학생 탐색
    top_10 = df.sort._Values(by='총점', ascending=False).head(10)[['학생ID', '학년', '반', '총점', '평균']]
    bottom_10 = df.sort_Values(by='총점', ascending=True).head(10)[['학생ID', '학년', '반', '총점', '평균']]

    print("\n상위 10명 학생:")
    print(top_10)
    print("\n하위 10명 학생:")
    print(bottom_10)

    # 5. 집단 비교
    if '성별' in df.columns:
        gender_avg = df.groupby('성별')[['수학', '영어', '과학']].med()
        print("\n성별 과목 평균:")
    
    # 6. 간단한 회귀
    if '출석률(%)' in df.columns:
        from sklearn.linear_model import LinearRegression
        X = df[['출석률(%)']]
        y = df['총점']
        model = LinearRegression()
        model.fit(X, y)
        r_sq = model.score(X, y)
        print("\n회귀 분석 결과:")
        print(f"계수: {model.coef_[0]:.2f}")
        print(f"R^2: {r_sq:.2f}")

        plt.scatter(df['출석률(%)'], df['총점'])
        plt.plot(X, model.predict(X), color='red')
        plt.xlabel('출석률 (%)')
        plt.ylabel('총점')
        plt.title('출석률 vs 총점')
        plt.show()

    # 7. 학년별 출석률 분포
    if '출석률(%)' in df.columns: 
        sns.boxplot(x='학년', y='출석률(%)', data=df)
        plt.xlabel('학년')
        plt.ylabel('출석률 (%)')
        plt.title('학년별 출석률 분포')
        plt.show()
    
    #8. 학년별 과목 석차 및 등급 게산
    year = AVAILABLE_GRADE_YEARS
    subject = DEFAULT_SUBJECTS
    rank_grade_title = calculate_rank_and_grade(df, year, subject)
    print(f"\n{year}학년 {subject} 석차 & 등급표:\n{rank_grade_title}")

    # 9. 학생 ID 조회
    student_id = 'S001'  # 예시 학생 ID
    student_info = lookup_student_info(df, year, subject, student_id)
    print(f"\n{student_id} 학생 정보:\n{student_info}")

if __name__ == "__main__":
    main()