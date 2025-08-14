SIPE 동아리의 멘토링을 받으며 수행하는 과제.

# 파일 구성도
- ```analysis.py```: 전체 분석 흐름을 관리, 필요한 모듈들을 호출하는 메인 파일
- ```config.py```: 등급 기준(5등급), 학년, 과목 선택 옵션 등을 설정하는 파일
- ```data_loader.py```: student_scores.csv 파일 로드하고 전처리하는 함수 정의
- ```grade_calculator.py```: 5등급 기준에 따라 등급을 계산하는 함수 정의
- ```rank_and_grade.py```: 학생 석차 및 등급을 계산하고 표로 출력하는 함수 정의
- ```report.md```: 분석 결과 요약 및 시각화 결과
- ```student_id_lookup.py```: 학년과 과목 선택 시 해당 학생들의 석차/등급 정보를 조회하는 함수 정의
- ```student_source.csv```: 학생 정보 및 성적 데이터

## 라이브러리 설치 터미널 명령어:
```pip install pandas numpy matplotlib seaborn scikit-learn```

## 필수 과제
1. **기술통계**
   - 과목별 평균/표준편차/최솟값/최댓값/사분위수 요약표 작성
   - 학년별 과목 평균 비교 표 작성

2. **관계 분석**
   - `출석률(%)`과 각 과목 점수 간 **피어슨 상관계수** 계산 및 해석
   - 과목 간 상관 행렬(heatmap) 시각화

3. **상위/하위 학생 탐색**
   - 학생별 `총점`, `평균` 컬럼 추가
   - 상위 10명과 하위 10명 표로 제시(학생ID, 학년/반, 총점, 평균)

4. **집단 비교**
   - 성별별 과목 평균 비교 막대그래프(또는 표)
   - 학년별 출석률 분포(박스플롯) 그래프

5. **간단한 회귀(선형)**
   - `출석률(%)` → `총점` 단순 선형회귀를 fit하여 계수, R² 출력
   - 회귀선이 포함된 산점도(출석률 vs 총점) 시각화

6. **결론 정리**
   - 인사이트 3가지 이상을 **문장**으로 요약

## 추가적으로 진행한 내용
- 등급 산출 기능: 5등급제에 따른 등급 계산 및 적용
- 학생 ID 조회 기능: 학년과 과목을 선택하여 해당 학생의 석차/등급 정보 조회
- 파일 구조 변경: 코드 가독성 및 유지보수성을 위해 파일 분리
  - 기존 ```analysis.py``` 파일만 존재
  - 변경 후 ```config, data_loader, grade_calculator, rank_and_grade, student_id__lookup, analysis```
- 설정 파일 활용: 등급 기준, 학년, 과목 선택 옵션을 설정 파일에서 관리

## 🚧 개발 과정에서 발생한 문제점과 어려움

### 1. pandas SettingWithCopyWarning 문제
**문제**: DataFrame 복사 시 발생하는 경고 메시지
```python
SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame
```

**원인**: DataFrame의 슬라이스에 직접 값을 할당할 때 발생
**해결 방법**: 
- `.copy()` 메서드를 사용하여 명시적 복사
- `.loc` 인덱서를 사용하여 안전한 값 할당
```python
# 수정 전
df_slice = df[condition]
df_slice['new_column'] = value

# 수정 후
df_slice = df[condition].copy()
df_slice.loc[:, 'new_column'] = value
```

### 2. 한글 폰트 표시 문제
**문제**: matplotlib에서 한글 텍스트가 깨져서 표시됨
**원인**: 기본 폰트가 한글을 지원하지 않음
**해결 방법**:
```python
plt.rcParams['font.family'] = ['Malgun Gothic', 'NanumGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
```

### 3. 함수 호출 시 잘못된 인자 전달
**문제**: `calculate_grade` 함수 호출 시 인자 개수 불일치
```python
# 오류 코드
year_df['등급'] = year_df[score_column].apply(lambda x: calculate_grade(x, GRADE_SYSTEM = "5등급"))
```

**해결 방법**: 함수 시그니처에 맞게 인자 수정
```python
# 수정된 코드
year_df_with_grades = assign_grades(year_df[['학생ID', '수학', '영어', '과학']])
year_df['등급'] = year_df_with_grades['등급']
```

### 4. 존재하지 않는 컬럼 참조 오류
**문제**: DataFrame에 존재하지 않는 컬럼을 참조하려 할 때 발생
**해결 방법**: 컬럼 존재 여부 확인 후 안전하게 접근
```python
available_columns = ['학생ID', '학년', score_column]
if '반' in student_info.columns:
    available_columns.append('반')
if '석차' in student_info.columns:
    available_columns.append('석차')
```

### 5. 학년별 등급 계산 로직 오류
**문제**: 전체 데이터에서 등급을 계산하여 학년별 구분이 안됨
**원인**: 등급 계산 시 학년별 필터링이 제대로 적용되지 않음
**해결 방법**: 학년별로 데이터를 분리한 후 각각 등급 계산
```python
year_df = df[df['학년'] == year].copy()
year_df_with_grades = assign_grades(year_df[['학생ID', '수학', '영어', '과학']])
```

### 6. 인터랙티브 입력 처리의 복잡성
**문제**: 사용자 입력 처리 시 예외 상황 고려 필요
**해결 방법**: try-except 구문과 입력 검증 로직 추가
```python
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
```

### 7. 모듈 간 의존성 관리
**문제**: 파일 분리 시 모듈 간 import 순서와 의존성 문제
**해결 방법**: 
- 명확한 import 구조 설계
- 순환 참조 방지
- 설정 파일을 통한 중앙 집중식 관리

### 8. 데이터 전처리 및 검증
**문제**: CSV 파일 로드 시 데이터 타입과 결측치 처리
**해결 방법**: 
- 데이터 타입 명시적 변환
- 결측치 확인 및 처리 로직 추가
- 데이터 유효성 검증

## 💡 학습한 내용

### 1. pandas DataFrame 조작
- 안전한 데이터 수정 방법
- SettingWithCopyWarning 이해 및 해결
- 효율적인 데이터 필터링과 그룹화

### 2. matplotlib 시각화
- 한글 폰트 설정 방법
- 다양한 그래프 타입 활용
- 시각화 커스터마이징

### 3. 모듈화 및 코드 구조
- 파일 분리를 통한 코드 재사용성 향상
- 설정 파일을 통한 유지보수성 개선
- 함수 설계 및 인터페이스 정의

### 4. 에러 처리 및 디버깅
- 예외 상황 처리 방법
- 사용자 입력 검증
- 코드 안정성 향상 기법

### 5. 데이터 분석 워크플로우
- EDA(탐색적 데이터 분석) 과정
- 통계적 분석 방법론
- 결과 해석 및 인사이트 도출

이러한 문제점들을 해결하면서 pandas, matplotlib, 데이터 분석에 대한 깊은 이해를 얻을 수 있었습니다.
