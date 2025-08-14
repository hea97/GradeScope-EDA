import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data
from grade_calculator import assign_grades, assign_subject_grades
from rank_and_grade import calculate_rank_and_grade
from student_id_lookup import lookup_student_info

# 설정 파일 로드
from config import GRADE_SYSTEM, AVAILABLE_GRADE_YEARS, DEFAULT_SUBJECTS

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'NanumGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def show_visualization_option(visualization_name):
    """시각화 보기 옵션을 제공하는 함수"""
    while True:
        choice = input(f"\n{visualization_name} 시각화를 보시겠습니까? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        else:
            print("y 또는 n을 입력해주세요.")

def interactive_student_lookup(df):
    """사용자가 학생 ID를 입력하여 조회할 수 있는 인터랙티브 기능"""
    print("\n" + "="*50)
    print("학생 ID 조회 기능")
    print("="*50)
    
    while True:
        print(f"\n사용 가능한 과목: {DEFAULT_SUBJECTS}")
        print(f"사용 가능한 학년: {AVAILABLE_GRADE_YEARS}")
        
        # 예시 학생 ID 보여주기
        example_student = df['학생ID'].iloc[0]
        print(f"예시 학생 ID: {example_student}")
        
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

def show_main_menu():
    """메인 메뉴를 표시하는 함수"""
    print("\n" + "="*70)
    print("🎓 GradeScope-EDA 학생 성적 분석 시스템")
    print("="*70)
    print("1. 필수 과제 분석")
    print("2. 추가 기능 분석") 
    print("3. 학생 ID 조회")
    print("="*70)

def main():
    df = load_data('student_scores.csv')
    
    # 총점 및 평균 계산
    df['총점'] = (df['수학'] + df['영어'] + df['과학']).round(1)
    df['평균'] = (df['총점'] / 3).round(1)
    
    # 등급 산출
    df_with_grades = assign_grades(df.copy())
    df['등급'] = df_with_grades['등급']

    show_main_menu()
    
    while True:
        choice = input("\n원하는 기능을 선택하세요 (1/2/3, 종료하려면 'q'): ").strip()
        
        if choice == 'q':
            print("프로그램을 종료합니다.")
            break
        elif choice == '1':
            print("\n" + "="*70)
            print("📊 1. 필수 과제 분석")
            print("="*70)
            
            # 1. 기술통계
            print("\n1️⃣ 기술 통계")
            print("-" * 50)
            print("과목별 기술 통계:")
            stat_df = df[['수학', '영어', '과학']].agg(['mean', 'std', 'min', 'max', lambda x:x.quantile(0.5)])
            print(stat_df.round(1))
            
            print("\n학년별 과목 평균 비교:")
            grade_subject_avg = df.groupby('학년')[['수학', '영어', '과학']].mean().round(1)
            print(grade_subject_avg)
            
            # 2. 관계 분석
            print("\n2️⃣ 관계 분석")
            print("-" * 50)
            if '출석률(%)' in df.columns:
                print("출석률과 과목 점수 간 피어슨 상관계수:")
                correlation = df[['출석률(%)', '수학', '영어', '과학']].corr()['출석률(%)'].round(3)
                print(correlation)
                
                # 과목 간 상관 행렬 시각화
                if show_visualization_option("과목 간 상관 행렬"):
                    plt.figure(figsize=(8, 6))
                    sns.heatmap(df[['수학', '영어', '과학']].corr(), annot=True, cmap='coolwarm', center=0)
                    plt.title('과목 간 상관 행렬')
                    plt.show()
            
            # 3. 상위/하위 학생 탐색
            print("\n3️⃣ 상위/하위 학생 탐색")
            print("-" * 50)
            top_10 = df.sort_values(by='총점', ascending=False).head(10)[['학생ID', '학년', '반', '총점', '평균']]
            bottom_10 = df.sort_values(by='총점', ascending=True).head(10)[['학생ID', '학년', '반', '총점', '평균']]

            print("상위 10명 학생:")
            print(top_10)
            print(f"상위 10명 평균 총점: {top_10['총점'].mean():.1f}, 평균: {top_10['평균'].mean():.1f}")
            print("\n하위 10명 학생:")
            print(bottom_10)
            print(f"하위 10명 평균 총점: {bottom_10['총점'].mean():.1f}, 평균: {bottom_10['평균'].mean():.1f}")
            
            # 4. 집단 비교
            print("\n4️⃣ 집단 비교")
            print("-" * 50)
            
            # 성별별 성적 비교
            if '성별' in df.columns:
                print("성별별 성적 비교:")
                gender_avg = df.groupby('성별')[['수학', '영어', '과학']].mean().round(1)
                print(gender_avg)
                
                if show_visualization_option("성별별 과목 평균"):
                    gender_avg.plot(kind='bar', figsize=(10, 6))
                    plt.title('성별별 과목 평균')
                    plt.xlabel('성별')
                    plt.ylabel('평균 점수')
                    plt.xticks(rotation=0)
                    plt.legend()
                    plt.tight_layout()
                    plt.show()
            
            # 학년별 성적 비교
            print("\n학년별 성적 비교:")
            year_avg = df.groupby('학년')[['수학', '영어', '과학']].mean().round(1)
            print(year_avg)
            
            if show_visualization_option("학년별 과목 평균"):
                year_avg.plot(kind='bar', figsize=(10, 6))
                plt.title('학년별 과목 평균')
                plt.xlabel('학년')
                plt.ylabel('평균 점수')
                plt.xticks(rotation=0)
                plt.legend()
                plt.tight_layout()
                plt.show()
            
            # 5. 간단한 회귀
            print("\n5️⃣ 간단한 회귀 분석")
            print("-" * 50)
            if '출석률(%)' in df.columns:
                from sklearn.linear_model import LinearRegression
                X = df[['출석률(%)']]
                y = df['총점']
                model = LinearRegression()
                model.fit(X, y)
                r_sq = model.score(X, y)
                print(f"출석률 → 총점 회귀 분석:")
                print(f"회귀 계수: {model.coef_[0]:.2f}")
                print(f"R²: {r_sq:.2f}")

                if show_visualization_option("출석률 vs 총점 회귀선"):
                    plt.figure(figsize=(8, 6))
                    plt.scatter(df['출석률(%)'], df['총점'], alpha=0.6)
                    plt.plot(X, model.predict(X), color='red', linewidth=2)
                    plt.xlabel('출석률 (%)')
                    plt.ylabel('총점')
                    plt.title('출석률 vs 총점 (회귀선 포함)')
                    plt.grid(True, alpha=0.3)
                    plt.show()
            
            # 6. 결론 정리
            print("\n6️⃣ 결론 정리 (인사이트)")
            print("-" * 50)
            print("1. 출석률과 수학 성적 간에는 약한 양의 상관관계(0.257)가 있어, 출석률이 높을수록 수학 성적이 좋은 경향을 보입니다.")
            print("2. 여학생이 남학생보다 모든 과목에서 평균적으로 높은 성적을 보이고 있습니다.")
            print("3. 상위 10명과 하위 10명의 성적 차이가 매우 크며, 교육 격차가 존재함을 확인할 수 있습니다.")
            print("4. 3학년이 1, 2학년보다 과학 과목에서 평균적으로 높은 성적을 보이고 있습니다.")
            
            print("\n✅ 필수 과제 분석이 완료되었습니다!")
            show_main_menu()
            
        elif choice == '2':
            print("\n" + "="*70)
            print("🔧 2. 추가 기능 분석")
            print("="*70)
            
            # 등급 산출 방식 안내
            print("\n📊 등급 산출 방식 안내")
            print("-" * 50)
            print("본 분석은 5등급 상대평가(상위 10%, 24%, 32%, 24%, 10%) 비율제 등급 산출 방식을 사용합니다.")
            
            # 학년 선택
            print("\n🏆 학년별 과목 상위 10명 조회")
            print("-" * 50)
            print("조회할 학년을 선택하세요:")
            for i, year in enumerate(AVAILABLE_GRADE_YEARS, 1):
                print(f"{i}. {year}학년")
            
            try:
                year_choice = int(input("학년 번호를 입력하세요: ")) - 1
                if 0 <= year_choice < len(AVAILABLE_GRADE_YEARS):
                    selected_year = AVAILABLE_GRADE_YEARS[year_choice]
                else:
                    print("잘못된 선택입니다. 1학년으로 기본 설정합니다.")
                    selected_year = 1
            except ValueError:
                print("잘못된 입력입니다. 1학년으로 기본 설정합니다.")
                selected_year = 1
            
            # 과목 선택
            print(f"\n{selected_year}학년의 조회할 과목을 선택하세요:")
            for i, subject in enumerate(DEFAULT_SUBJECTS, 1):
                print(f"{i}. {subject}")
            
            try:
                subject_choice = int(input("과목 번호를 입력하세요: ")) - 1
                if 0 <= subject_choice < len(DEFAULT_SUBJECTS):
                    selected_subject = DEFAULT_SUBJECTS[subject_choice]
                else:
                    print("잘못된 선택입니다. 수학으로 기본 설정합니다.")
                    selected_subject = "수학"
            except ValueError:
                print("잘못된 입력입니다. 수학으로 기본 설정합니다.")
                selected_subject = "수학"
            
            # 해당 학년의 데이터 필터링
            year_df = df[df['학년'] == selected_year].copy()
            
            if not year_df.empty:
                # 과목별 점수 컬럼 선택
                if selected_subject == "수학":
                    score_column = "수학"
                elif selected_subject == "영어":
                    score_column = "영어"
                else:
                    score_column = "과학"
                
                # 해당 학년 내에서 과목별 석차 계산
                year_df['과목석차'] = year_df[score_column].rank(ascending=False).astype(int)
                
                # 해당 학년 내에서 전체 성적 석차 계산
                year_df['전체석차'] = year_df['총점'].rank(ascending=False).astype(int)
                
                # 해당 학년 내에서 과목별 등급 계산
                year_df_with_subject_grades = assign_subject_grades(year_df, score_column)
                year_df['과목등급'] = year_df_with_subject_grades['등급']
                
                # 해당 학년 내에서 전체 성적 등급 계산
                year_df_with_total_grades = assign_grades(year_df[['학생ID', '수학', '영어', '과학']])
                year_df['전체등급'] = year_df_with_total_grades['등급']
                
                # 상위 10명 선택 (순서: 학생ID, 학년, 반, 과목성적, 과목석차, 전체석차, 과목등급, 전체등급)
                top_10 = year_df.nsmallest(10, '과목석차')[['학생ID', '학년', '반', score_column, '과목석차', '전체석차', '과목등급', '전체등급']]
                
                print(f"\n{selected_year}학년 {selected_subject} 상위 10명:")
                print("-" * 80)
                print(top_10.to_string(index=False))
                print("-" * 80)
                print(f"※ 과목석차: {selected_year}학년 {selected_subject} 내 석차")
                print(f"※ 전체석차: {selected_year}학년 전체 성적 내 석차")
                print(f"※ 과목등급: {selected_year}학년 {selected_subject} 기준 5등급")
                print(f"※ 전체등급: {selected_year}학년 전체 성적 기준 5등급")
            else:
                print(f"\n{selected_year}학년 데이터가 없습니다.")
            
            print("\n✅ 추가 기능 분석이 완료되었습니다!")
            show_main_menu()
                    
        elif choice == '3':
            interactive_student_lookup(df)
            print("\n✅ 학생 ID 조회가 완료되었습니다!")
            show_main_menu()
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")
            show_main_menu()

if __name__ == "__main__":
    main()