import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data
from grade_calculator import assign_grades
from rank_and_grade import calculate_rank_and_grade
from student_id_lookup import lookup_student_info

# 설정 파일 로드
from config import GRADE_SYSTEM, AVAILABLE_GRADE_YEARS, DEFAULT_SUBJECTS

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'NanumGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def interactive_student_lookup(df):
    """사용자가 학생 ID를 입력하여 조회할 수 있는 인터랙티브 기능"""
    print("\n" + "="*50)
    print("학생 ID 조회 기능")
    print("="*50)
    
    while True:
        print(f"\n사용 가능한 과목: {DEFAULT_SUBJECTS}")
        print(f"사용 가능한 학년: {AVAILABLE_GRADE_YEARS}")
        
        # 사용자 입력 받기
        student_id = input("\n조회할 학생 ID를 입력하세요 (종료하려면 'q' 입력): ").strip()
        
        if student_id.lower() == 'q':
            print("학생 조회를 종료합니다.")
            break
            
        if student_id not in df['학생ID'].values:
            print(f"'{student_id}' 학생을 찾을 수 없습니다. 다시 시도해주세요.")
            continue
            
        # 과목 선택
        print(f"\n{student_id} 학생의 조회할 과목을 선택하세요:")
        for i, subject in enumerate(DEFAULT_SUBJECTS, 1):
            print(f"{i}. {subject}")
        
        try:
            subject_choice = int(input("과목 번호를 입력하세요: ")) - 1
            if 0 <= subject_choice < len(DEFAULT_SUBJECTS):
                subject = DEFAULT_SUBJECTS[subject_choice]
            else:
                print("잘못된 선택입니다. 수학으로 기본 설정합니다.")
                subject = "수학"
        except ValueError:
            print("잘못된 입력입니다. 수학으로 기본 설정합니다.")
            subject = "수학"
        
        # 학년 정보 가져오기
        student_data = df[df['학생ID'] == student_id]
        if not student_data.empty:
            year = student_data['학년'].iloc[0]
            
            # 학생 정보 조회
            try:
                student_info = lookup_student_info(df, year, subject, student_id)
                if not student_info.empty:
                    print(f"\n{student_id} 학생 정보 ({year}학년 {subject}):")
                    print("-" * 40)
                    print(student_info.to_string(index=False))
                else:
                    print(f"\n{student_id} 학생의 {subject} 정보를 찾을 수 없습니다.")
            except Exception as e:
                print(f"\n학생 조회 중 오류: {e}")
        else:
            print(f"{student_id} 학생의 학년 정보를 찾을 수 없습니다.")

def main():
    df = load_data('student_scores.csv')

    # 1. 기술통계
    print("="*60)
    print("1. 과목별 기술 통계")
    print("="*60)
    stat_df = df[['수학', '영어', '과학']].agg(['mean', 'std', 'min', 'max', lambda x:x.quantile(0.5)])
    print(stat_df.round(1)) # 소수점 첫째자리

    # 학년별 과목 평균 비교
    print("\n" + "="*60)
    print("2. 학년별 과목 평균 비교")
    print("="*60)
    grade_subject_avg = df.groupby('학년')[['수학', '영어', '과학']].mean().round(1)
    print(grade_subject_avg)

    # 2. 총점 및 평균 계산
    df['총점'] = (df['수학'] + df['영어'] + df['과학']).round(1)
    df['평균'] = (df['총점'] / 3).round(1)

    # 3. 등급 산출
    df_with_grades = assign_grades(df.copy())
    df['등급'] = df_with_grades['등급']

    # 4. 상위/하위 학생 탐색
    print("\n" + "="*60)
    print("3. 상위/하위 학생 탐색")
    print("="*60)
    top_10 = df.sort_values(by='총점', ascending=False).head(10)[['학생ID', '학년', '반', '총점', '평균']]
    bottom_10 = df.sort_values(by='총점', ascending=True).head(10)[['학생ID', '학년', '반', '총점', '평균']]

    print("상위 10명 학생:")
    print(top_10)
    print(f"상위 10명 평균 총점: {top_10['총점'].mean():.1f}, 평균: {top_10['평균'].mean():.1f}")
    print("\n하위 10명 학생:")
    print(bottom_10)
    print(f"하위 10명 평균 총점: {bottom_10['총점'].mean():.1f}, 평균: {bottom_10['평균'].mean():.1f}")

    # 5. 관계 분석 - 출석률과 과목 점수 간 상관계수
    if '출석률(%)' in df.columns:
        print("\n" + "="*60)
        print("4. 관계 분석 - 출석률과 과목 점수 간 피어슨 상관계수")
        print("="*60)
        correlation = df[['출석률(%)', '수학', '영어', '과학']].corr()['출석률(%)'].round(3)
        print(correlation)
        
        # 과목 간 상관 행렬 시각화
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[['수학', '영어', '과학']].corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('과목 간 상관 행렬')
        plt.show()

    # 6. 집단 비교
    if '성별' in df.columns:
        print("\n" + "="*60)
        print("5. 집단 비교 - 성별별 과목 평균")
        print("="*60)
        gender_avg = df.groupby('성별')[['수학', '영어', '과학']].mean().round(1)
        print(gender_avg)
        
        # 성별별 과목 평균 막대그래프
        gender_avg.plot(kind='bar', figsize=(10, 6))
        plt.title('성별별 과목 평균')
        plt.xlabel('성별')
        plt.ylabel('평균 점수')
        plt.xticks(rotation=0)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    # 7. 간단한 회귀
    if '출석률(%)' in df.columns:
        print("\n" + "="*60)
        print("6. 간단한 회귀 분석 - 출석률 → 총점")
        print("="*60)
        from sklearn.linear_model import LinearRegression
        X = df[['출석률(%)']]
        y = df['총점']
        model = LinearRegression()
        model.fit(X, y)
        r_sq = model.score(X, y)
        print(f"회귀 계수: {model.coef_[0]:.2f}")
        print(f"R²: {r_sq:.2f}")

        plt.figure(figsize=(8, 6))
        plt.scatter(df['출석률(%)'], df['총점'], alpha=0.6)
        plt.plot(X, model.predict(X), color='red', linewidth=2)
        plt.xlabel('출석률 (%)')
        plt.ylabel('총점')
        plt.title('출석률 vs 총점 (회귀선 포함)')
        plt.grid(True, alpha=0.3)
        plt.show()

    # 8. 학년별 출석률 분포
    if '출석률(%)' in df.columns: 
        print("\n" + "="*60)
        print("7. 학년별 출석률 분포")
        print("="*60)
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='학년', y='출석률(%)', data=df)
        plt.xlabel('학년')
        plt.ylabel('출석률 (%)')
        plt.title('학년별 출석률 분포')
        plt.show()
    

    # 등급 산출 방식 안내
    print("\n" + "="*60)
    print("8. 등급 산출 방식 안내")
    print("="*60)
    print("본 분석은 5등급 상대평가(상위 10%, 24%, 32%, 24%, 10%) 비율제 등급 산출 방식을 사용합니다.")

    # 9. 학년별 과목 석차 및 등급 계산 (반복문으로 처리)
    print("\n" + "="*60)
    print("9. 학년별 과목 석차 및 등급 계산")
    print("="*60)
    for year in AVAILABLE_GRADE_YEARS:
        for subject in DEFAULT_SUBJECTS:
            try:
                rank_grade_result = calculate_rank_and_grade(df, year, subject)
                if not rank_grade_result.empty:
                    print(f"\n{year}학년 {subject} 석차 & 등급표 (상위 10명):")
                    print(rank_grade_result.head(10))
                else:
                    print(f"\n{year}학년 {subject}: 해당 학년 데이터가 없습니다.")
            except Exception as e:
                print(f"\n{year}학년 {subject} 처리 중 오류: {e}")

    # 10. 결론 정리 (인사이트)
    print("\n" + "="*60)
    print("10. 결론 정리 (인사이트)")
    print("="*60)
    print("1. 출석률과 수학 성적 간에는 약한 양의 상관관계(0.257)가 있어, 출석률이 높을수록 수학 성적이 좋은 경향을 보입니다.")
    print("2. 여학생이 남학생보다 모든 과목에서 평균적으로 높은 성적을 보이고 있습니다.")
    print("3. 상위 10명과 하위 10명의 성적 차이가 매우 크며, 교육 격차가 존재함을 확인할 수 있습니다.")
    print("4. 3학년이 1, 2학년보다 과학 과목에서 평균적으로 높은 성적을 보이고 있습니다.")

    # 11. 인터랙티브 학생 조회 기능
    interactive_student_lookup(df)

if __name__ == "__main__":
    main()