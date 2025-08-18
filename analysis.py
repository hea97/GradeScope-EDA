
# GradeScope-EDA: 메뉴 기반 학생 성적 분석 시스템
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import load_data
from grade_calculator import assign_grades
from rank_and_grade import calculate_rank_and_grade
from student_id_lookup import lookup_student_info
from config import GRADE_SYSTEM, AVAILABLE_GRADE_YEARS, DEFAULT_SUBJECTS

plt.rcParams['font.family'] = ['Malgun Gothic', 'NanumGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def show_main_menu():
    print("\n" + "="*70)
    print("🎓 GradeScope-EDA 학생 성적 분석 시스템")
    print("="*70)
    print("1. 필수 과제 분석")
    print("2. 추가 기능 분석")
    print("3. 학생 ID 조회")
    print("="*70)

def run_basic_analysis(df):
    print("\n1. 기술통계\n" + "-"*60)
    # 1. 기술통계
    print("\n📊 기술통계(과목별/학년별):")
    stat_df = df[['수학', '영어', '과학']].agg(['mean', 'std', 'min', 'max', lambda x:x.quantile(0.5)])
    stat_df.index = ['평균', '표준편차', '최솟값', '최댓값', '중앙값']
    print(stat_df.round(1))
    print("\n학년별 성적 비교:")
    print(df.groupby('학년')[['수학', '영어', '과학']].mean().round(1))
    show_plot = input("\n학년별 과목 평균 시각화를 보시겠습니까? (y/n): ").strip().lower()
    if show_plot == 'y':
        df.groupby('학년')[['수학', '영어', '과학']].mean().plot(kind='bar', figsize=(10, 6))
        plt.title('학년별 과목 평균')
        plt.xlabel('학년')
        plt.ylabel('평균 점수')
        plt.xticks(rotation=0)
        plt.legend()
        plt.tight_layout()
        plt.show()

    print("\n2. 관계 분석\n" + "-"*60)
    # 2. 관계 분석
    if '출석률(%)' in df.columns:
        print("출석률(%)과 각 과목 점수 간 피어슨 상관계수:")
        corr = df[['출석률(%)', '수학', '영어', '과학']].corr()['출석률(%)'].round(3)
        print(corr)
        show_plot = input("과목 간 상관 행렬(heatmap) 시각화를 보시겠습니까? (y/n): ").strip().lower()
        if show_plot == 'y':
            plt.figure(figsize=(8, 6))
            sns.heatmap(df[['수학', '영어', '과학']].corr(), annot=True, cmap='coolwarm', center=0)
            plt.title('과목 간 상관 행렬')
            plt.show()
    else:
        print("출석률(%) 데이터가 없습니다.")

    print("\n3. 상위/하위 학생 탐색\n" + "-"*60)
    # 3. 상위/하위 학생 탐색
    df['총점'] = (df['수학'] + df['영어'] + df['과학']).round(1)
    df['평균'] = (df['총점'] / 3).round(1)
    top_10 = df.sort_values(by='총점', ascending=False).head(10)[['학생ID', '학년', '반', '총점', '평균']]
    bottom_10 = df.sort_values(by='총점', ascending=True).head(10)[['학생ID', '학년', '반', '총점', '평균']]
    print("상위 10명:")
    print(top_10)
    print(f"상위 10명 평균 총점: {top_10['총점'].mean():.1f}, 평균: {top_10['평균'].mean():.1f}")
    print("\n하위 10명:")
    print(bottom_10)
    print(f"하위 10명 평균 총점: {bottom_10['총점'].mean():.1f}, 평균: {bottom_10['평균'].mean():.1f}")

    print("\n4. 집단 비교\n" + "-"*60)
    # 4. 집단 비교
    if '성별' in df.columns:
        print("성별별 과목 평균 비교 표:")
        gender_avg = df.groupby('성별')[['수학', '영어', '과학']].mean().round(1)
        print(gender_avg)
        show_plot = input("성별별 과목 평균 막대그래프를 보시겠습니까? (y/n): ").strip().lower()
        if show_plot == 'y':
            gender_avg.plot(kind='bar', figsize=(10, 6))
            plt.title('성별별 과목 평균')
            plt.xlabel('성별')
            plt.ylabel('평균 점수')
            plt.xticks(rotation=0)
            plt.legend()
            plt.tight_layout()
            plt.show()
        if '출석률(%)' in df.columns:
            show_plot = input("학년별 출석률 분포(박스플롯)를 보시겠습니까? (y/n): ").strip().lower()
            if show_plot == 'y':
                plt.figure(figsize=(8, 6))
                sns.boxplot(x='학년', y='출석률(%)', data=df)
                plt.xlabel('학년')
                plt.ylabel('출석률 (%)')
                plt.title('학년별 출석률 분포')
                plt.show()
    else:
        print("성별 데이터가 없습니다.")

    print("\n5. 간단한 회귀(선형)\n" + "-"*60)
    # 5. 간단한 회귀(선형)
    if '출석률(%)' in df.columns:
        from sklearn.linear_model import LinearRegression
        X = df[['출석률(%)']]
        y = df['총점']
        model = LinearRegression()
        model.fit(X, y)
        r_sq = model.score(X, y)
        print(f"출석률(%) → 총점 단순 선형회귀 계수: {model.coef_[0]:.2f}")
        print(f"R²: {r_sq:.2f}")
        show_plot = input("출석률 vs 총점 산점도(회귀선 포함)를 보시겠습니까? (y/n): ").strip().lower()
        if show_plot == 'y':
            plt.figure(figsize=(8, 6))
            plt.scatter(df['출석률(%)'], df['총점'], alpha=0.6)
            plt.plot(X, model.predict(X), color='red', linewidth=2)
            plt.xlabel('출석률 (%)')
            plt.ylabel('총점')
            plt.title('출석률 vs 총점 (회귀선 포함)')
            plt.grid(True, alpha=0.3)
            plt.show()
    else:
        print("출석률(%) 데이터가 없습니다.")

    print("\n6. 결론 정리\n" + "-"*60)
    # 6. 결론 정리
    print("1. 출석률과 수학 성적 간에는 약한 양의 상관관계(0.257)가 있어, 출석률이 높을수록 수학 성적이 좋은 경향을 보입니다.")
    print("2. 여학생이 남학생보다 모든 과목에서 평균적으로 높은 성적을 보이고 있습니다.")
    print("3. 상위 10명과 하위 10명의 성적 차이가 매우 크며, 교육 격차가 존재함을 확인할 수 있습니다.")
    print("4. 3학년이 1, 2학년보다 과학 과목에서 평균적으로 높은 성적을 보이고 있습니다.")
    print("\n✅ 필수 과제 분석이 완료되었습니다!\n")

def run_additional_analysis(df):

    print("\n" + "="*70)
    print("🛠️  2. 추가 기능 분석")
    print("="*70)
    print("\n📚 등급 산출 방식 안내\n" + "-"*50)
    print("본 분석은 5등급 상대평가(상위 10%, 24%, 32%, 24%, 10%) 비율제 등급 산출 방식을 사용합니다.")
    print("-"*50)
    print("🏆 학년별 과목 상위 10명 조회")
    print("-"*50)
    print("조회할 학년을 선택하세요:")
    for i, year in enumerate(AVAILABLE_GRADE_YEARS, 1):
        print(f"{i}. {year}학년")
    year_choice = input("학년 번호를 입력하세요: ").strip()
    try:
        year_idx = int(year_choice) - 1
        if 0 <= year_idx < len(AVAILABLE_GRADE_YEARS):
            year = AVAILABLE_GRADE_YEARS[year_idx]
        else:
            print("잘못된 입력입니다. 1학년으로 기본 설정합니다.")
            year = AVAILABLE_GRADE_YEARS[0]
    except ValueError:
        print("잘못된 입력입니다. 1학년으로 기본 설정합니다.")
        year = AVAILABLE_GRADE_YEARS[0]

    print(f"\n{year}학년의 조회할 과목을 선택하세요:")
    for i, subject in enumerate(DEFAULT_SUBJECTS, 1):
        print(f"{i}. {subject}")
    subject_choice = input("과목 번호를 입력하세요: ").strip()
    try:
        subject_idx = int(subject_choice) - 1
        if 0 <= subject_idx < len(DEFAULT_SUBJECTS):
            subject = DEFAULT_SUBJECTS[subject_idx]
        else:
            print("잘못된 입력입니다. 수학으로 기본 설정합니다.")
            subject = DEFAULT_SUBJECTS[0]
    except ValueError:
        print("잘못된 입력입니다. 수학으로 기본 설정합니다.")
        subject = DEFAULT_SUBJECTS[0]

    # 상위 10명 출력
    result = calculate_rank_and_grade(df, year, subject)
    if not result.empty:
        df_with_grades = assign_grades(df[df['학년'] == year].copy())
        df_with_grades['전체석차'] = df_with_grades['총점'].rank(ascending=False, method='min').astype(int)
        merged = df[df['학년'] == year][['학생ID', '학년', '반', subject]].merge(result, on='학생ID')
        merged = merged.merge(df_with_grades[['학생ID', '전체석차', '등급']], on='학생ID', how='left')
        merged = merged.rename(columns={'석차': '과목석차', '등급_x': '과목등급', '등급_y': '전체등급'})
        print(f"\n📋 {year}학년 {subject} 상위 10명")
        print()
        print("학생ID | 학년 | 반 | {0:4s} | 과목석차 | 전체석차 | 과목등급 | 전체등급".format(subject))
        for _, row in merged.sort_values(by='과목석차').head(10).iterrows():
            print(f"{row['학생ID']:6s} | {row['학년']:2d} | {row['반']:2s} | {row[subject]:3d} | {row['과목석차']:8d} | {row['전체석차']:8d} | {row['과목등급']:8d} | {row['전체등급']:8d}")
        print("\n※ 과목석차: {0}학년 {1} 내 석차".format(year, subject))
        print("※ 전체석차: {0}학년 전체 성적 내 석차".format(year))
        print("※ 과목등급: {0}학년 {1} 기준 5등급".format(year, subject))
        print("※ 전체등급: {0}학년 전체 성적 기준 5등급".format(year))
    else:
        print(f"{year}학년 {subject}: 해당 학년 데이터가 없습니다.")
    print("\n✅ 추가 기능 분석이 완료되었습니다!\n")



def run_student_id_lookup(df):
    print("\n" + "="*50)
    print("학생 ID 조회 기능")
    print("="*50)
    # 사용 가능한 과목: 수학, 영어, 과학, 전체
    subject_options = DEFAULT_SUBJECTS + ["전체"]
    print(f"사용 가능한 과목: {subject_options}")
    # 예시 학생 ID: S1000 ~ S1119
    print("예시 학생 ID: S1000 ~ S1119")

    while True:
        student_id = input("\n조회할 학생 ID를 입력하세요 (종료하려면 'q' 입력): ").strip()
        if student_id.lower() == 'q':
            print("학생 조회를 종료합니다.")
            break
        if student_id not in df['학생ID'].values:
            print(f"'{student_id}' 학생을 찾을 수 없습니다. 다시 시도해주세요.")
            continue
        # 과목 선택
        print(f"\n{student_id} 학생의 조회할 과목을 선택하세요:")
        for i, subject in enumerate(subject_options, 1):
            print(f"{i}. {subject}")
        try:
            subject_choice = int(input("과목 번호를 입력하세요: ")) - 1
            if 0 <= subject_choice < len(subject_options):
                subject = subject_options[subject_choice]
            else:
                print("잘못된 선택입니다. 수학으로 기본 설정합니다.")
                subject = "수학"
        except ValueError:
            print("잘못된 입력입니다. 수학으로 기본 설정합니다.")
            subject = "수학"
        student_data = df[df['학생ID'] == student_id]
        if not student_data.empty:
            year = student_data['학년'].iloc[0]
            try:
                if subject == "전체":
                    # 해당 학년 데이터만 사용
                    year_df = df[df['학년'] == year].copy()
                    if student_id not in year_df['학생ID'].values:
                        print(f"\n{student_id} 학생의 전체 성적 정보를 찾을 수 없습니다.")
                        continue
                    # 총점, 평균, 전체등급, 전체석차 계산
                    df_with_grades = assign_grades(year_df)
                    # 총점 기준 석차
                    df_with_grades['전체석차'] = df_with_grades['총점'].rank(ascending=False, method='min').astype(int)
                    # 과목별 등급
                    from grade_calculator import assign_subject_grades
                    subj_grades = {}
                    for subj in DEFAULT_SUBJECTS:
                        subj_df = assign_subject_grades(year_df[['학생ID', subj]], subj)
                        subj_grade = subj_df[subj_df['학생ID'] == student_id]['등급'].values[0]
                        subj_grades[subj] = subj_grade
                    row = df_with_grades[df_with_grades['학생ID'] == student_id]
                    # 출력
                    print(f"\n{student_id} 학생 정보 (전체):")
                    print("-" * 40)
                    # 학생ID, 반, 수학, 영어, 과학, 각 과목등급, 전체등급, 전체석차
                    info = [
                        f"학생ID: {student_id}",
                        f"학년: {row['학년'].values[0]}",
                        f"반: {row['반'].values[0]}",
                        f"수학: {row['수학'].values[0]} (등급 {subj_grades['수학']})",
                        f"영어: {row['영어'].values[0]} (등급 {subj_grades['영어']})",
                        f"과학: {row['과학'].values[0]} (등급 {subj_grades['과학']})",
                        f"총점: {int(row['총점'].values[0])}",
                        f"평균: {row['평균'].values[0]:.1f}",
                        f"전체등급: {row['등급'].values[0]}",
                        f"전체석차: {row['전체석차'].values[0]}"
                    ]
                    print("\n".join(info))
                else:
                    student_info = lookup_student_info(df, year, subject, student_id)
                    if not student_info.empty:
                        # 학년 정보 없이 출력
                        print(f"\n{student_id} 학생 정보 ({subject}):")
                        print("-" * 40)
                        # 학년 컬럼 제외
                        display_cols = [col for col in student_info.columns if col != '학년']
                        print(student_info[display_cols].to_string(index=False))
                    else:
                        print(f"\n{student_id} 학생의 {subject} 정보를 찾을 수 없습니다.")
            except Exception as e:
                print(f"\n학생 조회 중 오류: {e}")
        else:
            print(f"{student_id} 학생의 정보를 찾을 수 없습니다.")

def main():
    df = load_data('student_scores.csv')
    while True:
        show_main_menu()
        choice = input("\n원하는 기능을 선택하세요 (1/2/3, 종료하려면 'q'): ").strip()
        if choice == '1':
            run_basic_analysis(df)
        elif choice == '2':
            run_additional_analysis(df)
        elif choice == '3':
            run_student_id_lookup(df)
        elif choice.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1, 2, 3 또는 q 중에서 선택하세요.")

if __name__ == "__main__":
    main()